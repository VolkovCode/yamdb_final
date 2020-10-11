from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperuserPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser


class IsAuthorOrReadOnlyPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_superuser)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            role = request.user.role == 'admin' or request.user.is_superuser
            return bool(role)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            role = request.user.role == 'admin' or request.user.is_superuser
            return bool(role)


class IsAdminOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'admin' or request.user.is_superuser:
                return True


class IsAuthorOrAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            role = request.user.role == 'admin' \
                   or request.user.role == 'moderator' \
                   or obj.author == request.user
            return bool(role)
        elif request.method == "GET":
            return True
