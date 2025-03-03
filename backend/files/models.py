from django.db import models

# Create your models here.
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploaded-files/')
    uploadTime = models.DateTimeField(auto_now_add=True)

class fontFiles(models.Model):
    file = models.FileField(upload_to='font_files/')

    def __str__(self):
        return self.file.name