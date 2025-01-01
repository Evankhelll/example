from django.db import models

# Create your models here.
class gambar(models.Model):

    # Fields
    gambar = models.FileField(upload_to="upload/files/")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    nama_gambar = models.TextField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    keterangan = models.TextField(max_length=100)