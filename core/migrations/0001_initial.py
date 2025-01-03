# Generated by Django 5.1.4 on 2025-01-01 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='gambar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gambar', models.FileField(upload_to='upload/files/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('nama_gambar', models.TextField(max_length=100)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('keterangan', models.TextField(max_length=100)),
            ],
        ),
    ]
