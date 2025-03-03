
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .models import UploadedFile

def ffupload(request):
    if request.method == "POST":
        
        pass