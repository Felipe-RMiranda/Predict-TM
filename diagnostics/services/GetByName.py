import os
from rest_framework.response import Response
from ..repositorys import IDiagnosisRepository, DiagnosisRepository
from .Renders import Renders, IRenders
import logging

logger = logging.getLogger("django")

class IGetByName:
    def get(self, request):
        pass

class GetByName:
    @staticmethod
    def get(
            request,
            repo: IDiagnosisRepository = DiagnosisRepository(),
            render: IRenders = Renders()
    ):
        try:
            diag = repo.get_by_name(name=request.GET.get("name"))
            if diag is None:
                return render.up_form(request)
            return render.dashboard(request, diag)
        except Exception as e:
            logger.error(f"GetByName error: {e}")
            return Response({"error": "Ocorreu um erro interno"}, status=500)