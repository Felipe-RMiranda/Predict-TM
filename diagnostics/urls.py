from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    path('upForm/', views.upForm, name='upForm'),
    path('getDiagnosis/', views.getDiagnosis),
    path('deshboard/', views.deshboard),
    path('', include(router.urls)),
]