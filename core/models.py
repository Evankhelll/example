from django.db import models

# Create your models here.
class gambar(models.Model):

    # Fields
    nama_gambar = models.TextField(max_length=100)
    keterangan = models.TextField(max_length=100, blank=True, null=True)
    gambar = models.FileField(upload_to="upload/files/")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

class komentar(models.Model):

    # Fields
    nama = models.TextField(max_length=100)
    email = models.EmailField()
    komentar = models.TextField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)