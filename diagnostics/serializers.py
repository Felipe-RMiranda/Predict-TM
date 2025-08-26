from rest_framework import serializers
from .models import Paciente, Diagnostico
import base64
from django.core.files.base import ContentFile

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class DiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = '__all__'