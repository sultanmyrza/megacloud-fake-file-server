from rest_framework import serializers

from .models import MegaBinary, MegaFile


class MegaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MegaFile
        fields = "__all__"


class MegaBinarySerializer(serializers.ModelSerializer):
    class Meta:
        model = MegaBinary
        fields = ("data",)


class CreateDirectoryRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    dirId = serializers.CharField(max_length=200, allow_null=True)


class CreateDirectoryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MegaFile
        fields = ["id", "fileName", "type", "serverFileName", "addDate"]


class CreateFileRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    size = serializers.IntegerField()
    extension = serializers.CharField(max_length=150)
    dirId = serializers.CharField(max_length=200, allow_null=True)


class CreateFileResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MegaFile
        fields = [
            "id",
            "fileName",
            "serverFileName",
            "extension",
            "preview",
            "type",
            "uploadUrl",
            "addDate",
        ]


class GetTemporaryDownloadUrlRequest(serializers.Serializer):
    hour = serializers.IntegerField(min_value=1, max_value=168)


class GetTemporaryDownloadUrlResponse(serializers.ModelSerializer):
    class Meta:
        model = MegaFile
        fields = [
            "id",
            "fileName",
            "serverFileName",
            "extension",
            "preview",
            "type",
            "uploadUrl",
            "downloadUrl",
            "addDate",
        ]


class MegaListItemFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MegaFile
        fields = [
            "id",
            "fileName",
            "extension",
            "preview",
            "type",
            "uploadUrl",
            "serverFileName",
            "addDate",
        ]


class MegaListItemDirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MegaFile
        fields = [
            "id",
            "fileName",
            "type",
            "serverFileName",
            "addDate",
        ]


class RenameFileRequestSerializer(serializers.Serializer):
    fileName = serializers.CharField(max_length=120)


class RenameFileResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MegaFile
        fields = [
            "id",
            "fileName",
            "serverFileName",
            "extension",
            "preview",
            "type",
            "uploadUrl",
            "addDate",
        ]


class RenameFolderRequestSerializer(serializers.Serializer):
    dirName = serializers.CharField(max_length=120)


class RenameFolderResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MegaFile
        fields = [
            "id",
            "fileName",
            "type",
            "addDate",
        ]


class MoveFileRequestSerializer(serializers.Serializer):
    dirId = serializers.CharField()


class MoveFileResponseSerializer(serializers.Serializer):
    dir = RenameFolderResponseSerializer(read_only=True)

    class Meta:
        model = MegaFile
        fields = [
            "id",
            "fileName",
            "serverFileName",
            "extension",
            "preview",
            "type",
            "uploadUrl",
            "addDate",
            "dir",
        ]
