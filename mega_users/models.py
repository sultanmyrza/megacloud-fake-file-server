from django.db import models


class MegaRate(models.Model):
    name = models.CharField(max_length=255)
    volume_gb = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class MegaUser(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    external_id = models.CharField(max_length=255)
    rate = models.ForeignKey(MegaRate, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.id
