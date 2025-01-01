from rest_framework import serializers

from . import models


class gambarSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.gambar
        fields = [
            "gambar",
            "created",
            "nama_gambar",
            "last_updated",
            "keterangan",
        ]