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
    CreateFileRequestSerializer,
    CreateFileResponseSerializer,
)


@api_view(["POST"])
@check_mega_user_exists
def create_file_or_directory(request, user_external_id):
    create_file = request.data.get("extension") is not None

    if create_file:
        serializer = CreateFileRequestSerializer(data=request.data)
        if serializer.is_valid():
            mega_user = MegaUser.objects.get(external_id=user_external_id)
            parent_file = MegaFile.objects.filter(id=serializer.data["dirId"]).first()

            new_file = MegaFile()
            new_file.owner = mega_user
            new_file.fileName = serializer.data["name"]
            new_file.extension = serializer.data["name"].split(".")[-1]
            new_file.serverFileName = f"{uuid.uuid4().int}.{new_file.extension}"
            new_file.parent = parent_file
            new_file.type = "file"
            new_file.size = 0
            # TODO: make these fields optional or "" by default
            new_file.downloadUrl = ""
            new_file.uploadUrl = ""
            # TODO: for folder it might be folder image placeholder?
            new_file.preview = ""
            new_file.save()

            host = f"{ request.scheme }://{ request.META.get('HTTP_HOST') }"
            new_file.uploadUrl = f"{host}/{new_file.id}/{new_file.fileName}"
            new_file.save()

            data = CreateFileResponseSerializer(new_file).data

            return Response(data, status=status.HTTP_201_CREATED)
    else:
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
            new_file.uploadUrl = ""
            new_file.downloadUrl = ""
            # TODO: for folder it might be folder image placeholder?
            new_file.preview = ""

            new_file.save()

            data = CreateDirectoryResponseSerializer(new_file).data

            return Response(data, status=status.HTTP_201_CREATED)

    return Response(
        data={user_external_id: user_external_id},
        status=status.HTTP_304_NOT_MODIFIED,
    )


@api_view(["POST"])
@check_mega_user_exists
def create_file(request, user_external_id):
    serializer = CreateFileRequestSerializer(data=request.data)
    if serializer.is_valid():
        mega_user = MegaUser.objects.get(external_id=user_external_id)
        parent_file = MegaFile.objects.filter(id=serializer.data["dirId"]).first()

        new_file = MegaFile()
        new_file.owner = mega_user
        new_file.fileName = serializer.data["name"].split(".")[0]
        new_file.extension = serializer.data["name"].split(".")[-1]
        new_file.serverFileName = f"{uuid.uuid4().int}.${new_file.extension}"
        new_file.parent = parent_file
        new_file.type = "file"
        new_file.size = 0

        # TODO: generate upload url
        # TODO: make these fields optional or "" by default
        new_file.uploadUrl = ""
        new_file.downloadUrl = ""
        # TODO: for file it can be megacloud log in file?
        new_file.preview = ""

        new_file.save()

        new_file.uploadUrl = f"{new_file.id}/{new_file.serverFileName}"
        new_file.save()

        data = CreateDirectoryResponseSerializer(new_file).data
        return Response(data, status=status.HTTP_201_CREATED)


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
