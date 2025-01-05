from rest_framework import viewsets, permissions

from . import serializers
from . import models


class gambarViewSet(viewsets.ModelViewSet):
    """ViewSet for the gambar class"""

    queryset = models.gambar.objects.all()
    serializer_class = serializers.gambarSerializer

class gambarViewSet(viewsets.ModelViewSet):
    """ViewSet for the gambar class"""

    queryset = models.komentar.objects.all()
    serializer_class = serializers.komentarSerializer