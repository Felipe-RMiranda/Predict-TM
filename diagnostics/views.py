from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import serializers
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import logging
from django.contrib.staticfiles.storage import staticfiles_storage
from .services import IGenerateDiagnosesService, GenerateDiagnosesService, GetByName, IGetByName, IRenders, Renders

logger = logging.getLogger("django")

@api_view(['GET'])
def homePage(request, render: IRenders = Renders()):
    return render.render_home(request=request)

@api_view(['POST'])
def diagnosis_generation(request, diagnoses: IGenerateDiagnosesService = GenerateDiagnosesService()):
    return diagnoses.generete(request=request)
@api_view(['GET'])
def get_diagnosis_by_name(request, get_name: IGetByName = GetByName()):
    return get_name.get(request=request)
