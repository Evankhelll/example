from rest_framework import serializers

from . import models


class gambarSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.gambar
        fields = [
            "id",
            "nama_gambar",
            "keterangan",
            "gambar",
            "created",
            "last_updated",
        ]