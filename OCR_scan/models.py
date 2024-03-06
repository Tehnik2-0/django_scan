from django.db import models


class Scan(models.Model):
    title = models.CharField(max_length=150)
    cover = models.ImageField(upload_to='images/')
    file = models.ForeignKey('Download', on_delete=models.CASCADE, null=False)
    text = models.TextField(null=True)

    def __str__(self):
        return self.title


class Download(models.Model):
    object_builbing = models.ForeignKey('ObjectBuilbing', on_delete=models.CASCADE, null=False, verbose_name='Объект строительства')
    file = models.FileField(upload_to='scan/', null=True, blank=True, verbose_name='Файл')
    task = models.ForeignKey('Task', on_delete=models.CASCADE, null=True)
    date_building = models.ForeignKey('DateBuilding', on_delete=models.CASCADE, null=False, verbose_name='Дата строительства')


class Task(models.Model):
    len_files = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)


class ObjectBuilbing(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DateBuilding(models.Model):
    date = models.CharField(max_length=255)

    def __str__(self):
        return self.date
