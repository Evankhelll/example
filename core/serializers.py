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

class komentarSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.komentar
        fields = [
            "id",
            "nama",
            "email",
            "komentar",
            "created",
            "last_updated",
        ]