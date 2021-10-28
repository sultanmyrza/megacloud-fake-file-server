import uuid

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .decorators import check_mega_user_existance
from .models import MegaRate, MegaUser
from .serializers import MegaUserReadSerializer


@api_view(["GET"])
@check_mega_user_existance
def get_user_info(request, external_id):
    mega_user = MegaUser.objects.get(external_id=external_id)
    return Response(
        data=MegaUserReadSerializer(mega_user).data,
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def create_user(request, external_id):
    response_status = status.HTTP_200_OK

    mega_user, created = MegaUser.objects.get_or_create(external_id=external_id)

    if created:
        response_status = status.HTTP_201_CREATED
        free_rate, _ = MegaRate.objects.get_or_create(name="FREE 1GB", volume_gb=1)

        mega_user.id = uuid.uuid4()
        mega_user.rate = free_rate
        mega_user.save()

    return Response(data=mega_user, status=response_status)
