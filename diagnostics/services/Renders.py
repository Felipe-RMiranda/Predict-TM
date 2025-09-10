from abc import ABC, abstractmethod
from django.shortcuts import render
from .ImgService import IImgService, ImgService
import logging
logger = logging.getLogger("django")

class IRenders(ABC):
    @abstractmethod
    def up_form(self, request):
        pass

    @abstractmethod
    def render_home(self, request):
        pass

    @abstractmethod
    def dashboard(self, request, diag):
        pass

class Renders(IRenders):
    def up_form(self, request): return render(request, 'up_form.html')

    def render_home(self, request): return render(request, 'index.html')

    def dashboard(self, request, diag,
                  service: IImgService = ImgService()):
        context = {
            'name': diag.name,
            'age': diag.age,
            'gender': diag.gender,
            'img': service.to_base64(diag.img),
            'probability': diag.probability,
            'status': diag.status,
            'result': diag.result
        }

        logger.info(f"\n🧠 Resultado da análise: {diag.result}")
        return render(request, 'dashboard.html', context)