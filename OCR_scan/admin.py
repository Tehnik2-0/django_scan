from django.contrib import admin

from .models import Scan, Download, ObjectBuilbing, DateBuilding, Task

admin.site.register(Scan)
admin.site.register(Download)
admin.site.register(ObjectBuilbing)
admin.site.register(DateBuilding)
admin.site.register(Task)