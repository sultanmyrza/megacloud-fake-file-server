from rest_framework import serializers
from .models import MegaRate, MegaUser


class MegaRateReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = MegaRate
        exclude = ("id",)


class MegaUserReadSerializer(serializers.ModelSerializer):
    rate = MegaRateReadOnlySerializer(read_only=True)

    class Meta:
        model = MegaUser
        fields = "__all__"
