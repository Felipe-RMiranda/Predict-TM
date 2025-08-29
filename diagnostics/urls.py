from django.urls import path, include
from grpc import services
from rest_framework.routers import DefaultRouter
from . import views
from .services.Renders import Renders, IRenders

router = DefaultRouter()
render: IRenders = Renders()
urlpatterns = [
    path('', render.render_home, name='renderHome'),
    path('getDiagnosisByName/', views.get_diagnosis_by_name, name='getDiagnosisByName'),
    path('upForm/', render.up_form, name='upForm'),
    path('diagnosisGeneration/', views.diagnosis_generation, name='diagnosisGeneration'),
    path('deshboard/', render.dashboard),
]