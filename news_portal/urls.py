from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from news.views import (
    NewsListCreateView,
    NewsDetail,
    CommentListCreateView,
    CommentDetail,
    StatusesListCreate,
    StatusesDetail,
    NewsStatusCreateView,
    CommentStatusCreateView
)


schema_view = get_schema_view(
   openapi.Info(
      title=" API",
      default_version='v0.1',
      description="API",
      terms_of_service="-",
      contact=openapi.Contact(email="-"),
      license=openapi.License(name="No License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


# router = DefaultRouter()
# router.register('news', NewsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/auth/token/', obtain_auth_token),
    path('', include('account.urls')),
    path('api/news/', NewsListCreateView.as_view()),
    path('api/news/<int:news_id>/', NewsDetail.as_view()),
    path('api/news/<int:news_id>/comments/', CommentListCreateView.as_view()),
    path('api/news/<int:news_id>/comments/<pk>/', CommentDetail.as_view()),
    path('api/statuses/', StatusesListCreate.as_view()),
    path('api/statuses/<int:pk>', StatusesDetail.as_view()),
    path('api/news/<news_id>/<slug>/', NewsStatusCreateView.as_view()),
    path('api/news/<int:news_id>/comments/<comment_id>/<slug>/', CommentStatusCreateView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_ui'),

]
