from django.shortcuts import get_object_or_404
from rest_framework import permissions
from operator import eq
from apps.papers.models import Paper

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        return obj.owner == request.user


class IsOwnerOrIsAuthenticatdThenCreateOnlyOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    message = "It's not permissioned"

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        UPDATE_METHODS = ('PUT', 'PATCH')

        if request.method in permissions.SAFE_METHODS:
            return True
        elif eq(request.method, 'POST') or eq(request.method, 'DELETE'):
            return  request.user and request.user.is_authenticated
        elif request.method in UPDATE_METHODS:
            return obj.author == request.user

        # Other method does not permissioned.
        return False


class IsAuthenticated(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        return super(IsAuthenticated, self).has_permission(request, view)

class PaperPermission(permissions.BasePermission):
    message = "It's not permissioned"

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        UPDATE_METHODS = ('PUT', 'PATCH')

        if view.action == 'admin':
            return request.user and request.user.is_authenticated and request.user == obj.author

        if request.method in permissions.SAFE_METHODS:
            return True
        elif eq(request.method, 'POST') or eq(request.method, 'DELETE'):
            return request.user and request.user.is_authenticated
        elif request.method in UPDATE_METHODS:
            return obj.author == request.user

        # Other method does not permissioned.
        return False

class ParticipatePermission(IsOwnerOrIsAuthenticatdThenCreateOnlyOrReadOnly):
    def has_permission(self, request, view):
        MODIFYING_METHODS = ('PUT', 'PATCH', "POST")

        if  request.method in MODIFYING_METHODS:
            if request.data.get("paper") == False:
                return False
            paper_id = request.data.get("paper")
            target_paper = get_object_or_404(Paper, pk=paper_id)
            if target_paper.is_finished:
                return False

        return True
