import uuid
from datetime import timedelta
from wsgiref.util import FileWrapper

from django.conf import settings
from django.db.models import F
from django.http import HttpResponse
from django.utils import timezone
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
    GetTemporaryDownloadUrlRequest,
    GetTemporaryDownloadUrlResponse,
    MegaListItemDirectorySerializer,
    MegaListItemFileSerializer,
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
    return Response(status=status.HTTP_200_OK)


@api_view(["POST", "DELETE"])
@check_mega_user_exists
def specific_file_related_actions(request, file_id, user_external_id):
    if request.method == "POST":
        return get_temporary_download_url(request, file_id, user_external_id)

    if request.method == "DELETE":
        return delete_by_id_file_or_directory(request, file_id, user_external_id)


def get_temporary_download_url(request, file_id, user_external_id):
    # get mega file
    serializer = GetTemporaryDownloadUrlRequest(data=request.data)
    if serializer.is_valid():
        mega_file = MegaFile.objects.get(id=file_id)
        hours = serializer.data["hour"]

        if settings.DEBUG:
            hours_added = timedelta(seconds=hours)
        else:
            hours_added = timedelta(hours=hours)

        downloadUrlExpireDate = timezone.now() + hours_added

        time_before = timezone.now().strftime("%m/%d/%Y, %H:%M:%S")
        time_after = downloadUrlExpireDate.strftime("%m/%d/%Y, %H:%M:%S")
        print(time_before)
        print(time_after)

        mega_file.downloadUrlExpireDate = downloadUrlExpireDate

        host = f"{ request.scheme }://{ request.META.get('HTTP_HOST') }"
        downloadUrl = f"{host}/{user_external_id}/{mega_file.serverFileName}"
        mega_file.downloadUrl = downloadUrl
        mega_file.downloadUrlExpireDate = downloadUrlExpireDate
        mega_file.save()
        data = GetTemporaryDownloadUrlResponse(mega_file).data
        # create serializer & pass as resposne

        return Response(data=data, status=status.HTTP_200_OK)

    # TODO: change to appropriate response
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@check_mega_user_exists
def download_file(request, user_external_id, server_file_name):
    mega_file = MegaFile.objects.get(serverFileName=server_file_name)
    mega_user = MegaUser.objects.get(external_id=user_external_id)

    if mega_file.owner.id != mega_user.id:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    expire_time = mega_file.downloadUrlExpireDate
    current_time = timezone.now()

    exp = expire_time.strftime("%m/%d/%Y, %H:%M:%S")
    cur = current_time.strftime("%m/%d/%Y, %H:%M:%S")
    print(exp)
    print(cur)
    # current_time = utc.localize(datetime.now())

    if expire_time < current_time:

        return HttpResponse(
            f"""<?xml version="1.0" encoding="UTF-8"?>
                <Error>
                    <Code>AccessDenied</Code>
                    <Message>Request has expired</Message>
                    <Key>{mega_file.fileName}</Key>
                    <BucketName>06458601-7608-476e-86c5-42adc0c8aadb</BucketName>
                    <Resource>{request.get_full_path()}</Resource>
                    <RequestId>15CD363501E4EFEB</RequestId>
                    <HostId>f687be98-fc29-4e53-bc4c-a540f9e0c193</HostId>
                </Error>
            """,
            content_type="text/xml",
        )

    document = open(mega_file.binary.data.path, "rb")
    response = HttpResponse(FileWrapper(document), content_type="*/*")
    response["Content-Disposition"] = 'attachment; filename="%s"' % mega_file.fileName
    return response


@api_view(["GET"])
@check_mega_user_exists
def get_files_from_root_directory(request, user_external_id):
    # get mega user
    mega_user = MegaUser.objects.get(external_id=user_external_id)

    # TODO: get sort direction
    limit = int(request.query_params.get("limit", "10"))
    offset = int(request.query_params.get("offset", "0"))
    direction = request.query_params.get("direction", "asc")
    field = request.query_params.get("field", "addDate")

    mega_files = (
        mega_user.files.order_by(F(field).asc())
        if direction == "asc"
        else mega_user.files.order_by(F(field).desc())
    )

    start = offset
    end = min(offset + limit, len(mega_files))
    mega_files = mega_files[start:end]

    data = []
    for item in mega_files:
        if item.type == "directory":
            data.append(MegaListItemDirectorySerializer(item).data)
        else:
            data.append(MegaListItemFileSerializer(item).data)

    return Response(
        data=data,
        status=status.HTTP_200_OK,
    )


@api_view(["GET", "DELETE"])
@check_mega_user_exists
def specific_directory_related_actions(request, dir_id, user_external_id):
    if request.method == "GET":
        return get_files_from_specific_directory(request, dir_id, user_external_id)
    elif request.method == "DELETE":
        return delete_directory_with_its_children(request, dir_id, user_external_id)


def get_files_from_specific_directory(request, dir_id, user_external_id):
    # get mega user
    mega_user = MegaUser.objects.get(external_id=user_external_id)

    # TODO: get sort direction
    limit = int(request.query_params.get("limit", "10"))
    offset = int(request.query_params.get("offset", "0"))
    direction = request.query_params.get("direction", "asc")
    field = request.query_params.get("field", "addDate")

    mega_files = mega_user.files.filter(parent__id=dir_id)

    mega_files = (
        mega_files.order_by(F(field).asc())
        if direction == "asc"
        else mega_files.order_by(F(field).desc())
    )

    start = offset
    end = min(offset + limit, len(mega_files))
    mega_files = mega_files[start:end]

    data = []
    for item in mega_files:
        if item.type == "directory":
            data.append(MegaListItemDirectorySerializer(item).data)
        else:
            data.append(MegaListItemFileSerializer(item).data)

    return Response(
        data=data,
        status=status.HTTP_200_OK,
    )


def delete_directory_with_its_children(request, dir_id, user_external_id):
    files_to_crawl = [MegaFile.objects.get(id=dir_id)]
    files_to_deleted = []

    while len(files_to_crawl) > 0:
        curr_file = files_to_crawl.pop()
        curr_file_children = MegaFile.objects.filter(parent_id=curr_file.id)
        files_to_crawl.extend(curr_file_children)

        files_to_deleted.append(curr_file)

    for f in files_to_deleted:
        f.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


def delete_by_id_file_or_directory(request, file_id, user_external_id):
    # TODO: check if file belongs to user
    MegaFile.objects.get(id=file_id).delete()
    # TODO: delete binary file to free disk space
    return Response(status=status.HTTP_204_NO_CONTENT)
