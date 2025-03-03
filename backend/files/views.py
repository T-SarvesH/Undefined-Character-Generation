# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .models import UploadedFile

@csrf_exempt
def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        uploaded_file = UploadedFile.objects.create(file=file)

        return JsonResponse({"message": "File uploaded successfully", "file_url": uploaded_file.file.url})

    return JsonResponse({"error": "No file uploaded"}, status=400)

def list_files(request):
    files = UploadedFile.objects.all()
    file_urls = [{"name": file.file.name, "url": file.file.url} for file in files]
    return JsonResponse({"files": file_urls})