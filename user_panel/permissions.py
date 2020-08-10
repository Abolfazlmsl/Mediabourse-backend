from datetime import datetime
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions

from bourse.models import WatchList


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsWatchListOwner(permissions.BasePermission):
    """
    only allow owner of an watch list add an object to it.
    """

    def has_permission(self, request, view):
        if request.POST:
            watch_list_id = request.POST.get('watch_list')
            user = request.user
            watch_list_object = WatchList.objects.filter(user=user).exists()
            return watch_list_object
        return True
