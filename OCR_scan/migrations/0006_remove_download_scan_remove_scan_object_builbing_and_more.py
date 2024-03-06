# Generated by Django 5.0.2 on 2024-03-03 21:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OCR_scan', '0005_task_download_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='download',
            name='scan',
        ),
        migrations.RemoveField(
            model_name='scan',
            name='object_builbing',
        ),
        migrations.RemoveField(
            model_name='scan',
            name='scan',
        ),
        migrations.AddField(
            model_name='download',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='scan/'),
        ),
        migrations.AddField(
            model_name='scan',
            name='file',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='OCR_scan.download'),
            preserve_default=False,
        ),
    ]