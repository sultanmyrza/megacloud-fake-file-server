import uuid

from mega_users.decorators import check_mega_user_exists
from mega_users.models import MegaUser
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response

from .models import MegaBinary, MegaFile
from .parser import BinaryFileParser
from .serializer import (
    CreateDirectoryRequestSerializer,
    CreateDirectoryResponseSerializer,
)


@api_view(["POST"])
@check_mega_user_exists
def create_directory(request, user_external_id):
    serializer = CreateDirectoryRequestSerializer(data=request.data)
    if serializer.is_valid():

        mega_user = MegaUser.objects.get(external_id=user_external_id)
        parent_file = MegaFile.objects.filter(id=serializer.data["dirId"]).first()

        new_file = MegaFile()
        new_file.owner = mega_user
        new_file.fileName = serializer.data["name"].split(".")[0]
        new_file.extension = "directory"
        new_file.serverFileName = f"{uuid.uuid4().int}"
        new_file.parent = parent_file
        new_file.type = "directory"
        new_file.size = 0

        # TODO: make these fields optional or "" by default
        new_file.preview = ""
        new_file.uploadUrl = ""
        new_file.downloadUrl = ""

        new_file.save()

        data = CreateDirectoryResponseSerializer(new_file).data
        return Response(data, status=status.HTTP_201_CREATED)

    return Response(
        data={user_external_id: user_external_id},
        status=status.HTTP_200_OK,
    )


@api_view(["PUT"])
@parser_classes([BinaryFileParser])
@check_mega_user_exists
def upload_mega_binary_file(request, mega_file_id, file_name, format=None):
    binary_data = request.data["file"]

    mega_binary_file = MegaBinary()
    mega_binary_file.data = binary_data
    mega_binary_file.save()

    # TODO: handel object does not exist case
    mega_file = MegaFile.objects.get(id=mega_file_id)
    mega_file.binary = mega_binary_file
    mega_file.save()

    # TODO: generate json reponse
    return Response(status=status.HTTP_201_CREATED)
