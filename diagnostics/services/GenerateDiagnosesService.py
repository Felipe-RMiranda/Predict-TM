import os
from abc import ABC, abstractmethod
from .AIService import AIService, IAIService
from ..serializers import DiagnosisRequestSerializer
from .Renders import Renders, IRenders
from ..repositorys import IDiagnosisRepository, DiagnosisRepository
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
import logging

logger = logging.getLogger("django")

class IGenerateDiagnosesService(ABC):
    @abstractmethod
    def generete(self, request):
        pass

class GenerateDiagnosesService(IGenerateDiagnosesService):
    @staticmethod
    def _predict(img, service: IAIService = AIService()):
        return service.img_predict(img)

    @staticmethod
    def _save(name, age, gender, img_bytes, prob, status_c, result,
              repo: IDiagnosisRepository = DiagnosisRepository()):
        repo.save(name, age, gender, img_bytes, prob, status_c, result)
        return repo.get_by_name(name)

    def generete(self, request, render: IRenders = Renders()):
        serializer = DiagnosisRequestSerializer(data=request.data)
        try:
            if serializer.is_valid():
                data = serializer.validated_data
                name = data["name"]
                age = data["age"]
                gender = data["gender"]
                img = data["img"]

                img_bytes = img.read()
                prob, result, status_c = self._predict(img_bytes)

                diag = self._save(name, age, gender, img_bytes, prob, status_c, result)
                return render.dashboard(request, diag)
            else:
                return JsonResponse({"success": False, "message": "preencha todos os campos" })
        except Exception as e:
            logger.error(f"GenerateDiagnosesService error: {e}")
            return Response({"error": "Erro interno no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)