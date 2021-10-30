from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response

from .models import MegaUser


def check_mega_user_exists(function):
    def wrap(request, *args, **kwargs):
        try:
            user_external_id = kwargs["user_external_id"]
            MegaUser.objects.get(external_id=user_external_id)
        except MegaUser.DoesNotExist:
            data = {"id": user_external_id, "message": "Can't find this user"}
            return Response(status=status.HTTP_409_CONFLICT, data=data)
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def check_mega_user_rate(function):
    def wrap(request, *args, **kwargs):
        mega_user = MegaUser.objects.get(pk=kwargs["entry_id"])
        if mega_user.rate is None:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
