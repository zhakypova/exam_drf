from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated


#
class IsAuthorOrReadOnly(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.author.user == request.user
        return False


class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author.user == request.user


class IsAdminStaffUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or request.user and request.user.is_staff)

# class IsAuthorOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True
#         return bool(request.user and request.user.is_authenticated)
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True
#         else:
#             bool(request.user and request.user.is_authenticated and obj.author == request.user)
