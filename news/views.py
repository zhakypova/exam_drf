from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Author
from .models import News, Comment, Status, NewsStatus, CommentStatus
from .serializers import NewsSerializer, CommentSerializer, StatusSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from .permissions import IsAuthorOrReadOnly, IsCommentAuthor, IsAdminStaffUser


class NewsListCreateView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['title', ]
    ordering_fields = ['created', ]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        author, _ = Author.objects.get_or_create(user=self.request.user)
        serializer.save(author=author)


class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs.get('news_id'))


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    pagination_class = LimitOffsetPagination

    # def get_queryset(self):
    #     return super().get_queryset().filter(news_id=self.kwargs.get('news_id'))

    def perform_create(self, serializer):
        news_id = self.kwargs.get('news_id')
        serializer.save(author=self.request.user.author, news_id=news_id)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthor, ]

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs.get('pk'))


class StatusesListCreate(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAdminStaffUser, ]

    def perform_create(self, serializer):
        serializer.save(
            news_id=self.kwargs.get('news_id'),
            author=self.request.user.author
        )


class StatusesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAdminUser, ]

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs.get('pk'))

    def get(self, request, news_id, slug):
        try:
            news = News.objects.get(id=news_id)
            if request.user != news.author.user:
                return Response({'error': 'You do not have permission to add status'}, status=status.HTTP_403_FORBIDDEN)
            news_status = NewsStatus.objects.filter(news=news, status__slug=slug)
            if news_status.exists():
                return Response({'error': 'You already added status'}, status=status.HTTP_400_BAD_REQUEST)
            status_obj, created = Status.objects.get_or_create(slug=slug)
            NewsStatus.objects.create(news=news, status=status_obj, author=news.author)
            return Response({'message': 'Status added'}, status=status.HTTP_201_CREATED)
        except News.DoesNotExist:
            return Response({'error': 'News not found'}, status=status.HTTP_404_NOT_FOUND)


class NewsStatusCreateView(APIView):
    permission_classes = [IsAuthorOrReadOnly]

    def post(self, request, *args, **kwargs):
        news = get_object_or_404(News, id=kwargs.get('news_id'))
        if news.author != request.user:
            return Response({"error": "You are not the author of this News."}, status=status.HTTP_403_FORBIDDEN)

        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(news=news, author=request.user)
            return Response({"message": "Status added"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentStatusCreateView(APIView):
    permission_classes = [IsAuthorOrReadOnly]

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=kwargs.get('comment_id'))
        if comment.author != request.user:
            return Response({"error": "You are not the author of this Comment."}, status=status.HTTP_403_FORBIDDEN)

        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(comment=comment, author=request.user)
            return Response({"message": "Status added"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)