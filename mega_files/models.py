import uuid

from django.db import models
from mega_users.models import MegaUser


class MegaBinary(models.Model):
    data = models.FileField(upload_to="bin/", blank=True)

    def __str__(self) -> str:
        return f"id: {self.pk}, serverFileName: ${self.data.name}"


class MegaFile(models.Model):
    owner = models.ForeignKey(MegaUser, related_name="files", on_delete=models.DO_NOTHING)
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=255)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    binary = models.OneToOneField(
        MegaBinary, on_delete=models.CASCADE, blank=True, null=True
    )
    fileName = models.CharField(max_length=255 - 16)
    serverFileName = models.CharField(max_length=255 - 16, default=uuid.uuid4().int)
    extension = models.CharField(max_length=16)
    type = models.CharField(max_length=255)
    size = models.BigIntegerField()
    preview = models.CharField(max_length=512, default="", blank=True)
    uploadUrl = models.CharField(max_length=512, default="", blank=True)
    downloadUrl = models.CharField(max_length=512, default="", blank=True)
    downloadUrlExpireDate = models.DateTimeField(auto_now_add=True, blank=True)
    addDate = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     self.serverFileName = f"{uuid.uuid4().int}.{self.extension}"
    #     super(MegaFile, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.fileName
