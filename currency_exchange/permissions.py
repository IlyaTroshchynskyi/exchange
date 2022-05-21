"""
    Collect custom permissions
"""

from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it see it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        """
        Instance must have an attribute named `owner`.
        :param request: request
        :param view: view
        :param obj: instance model
        :return: bool
        """
        return obj.username == request.user.username
