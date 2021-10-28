from mega_users.decorators import check_mega_user_existance
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response

from .models import MegaBinary, MegaFile
from .parser import BinaryFileParser
from .serializer import CreateDirectoryRequestSerializer


@api_view(["POST"])
@check_mega_user_existance
def create_directory(request, user_id):
    serializer = CreateDirectoryRequestSerializer(request.data)
    if serializer.is_valid():
        # TODO: create directory assigned to user
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(
        data={user_id: user_id},
        status=status.HTTP_200_OK,
    )


@api_view(["PUT"])
@parser_classes([BinaryFileParser])
@check_mega_user_existance
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
