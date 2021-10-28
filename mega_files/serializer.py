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
