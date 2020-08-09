from datetime import datetime
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
