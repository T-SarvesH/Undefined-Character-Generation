from django.contrib import admin
from .models import UploadedFile, fontFiles

# Register your models here.
admin.site.register(UploadedFile)
admin.site.register(fontFiles)