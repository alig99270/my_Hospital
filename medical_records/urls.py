# medical_records/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicalRecordViewSet

router = DefaultRouter()
router.register(r'records', MedicalRecordViewSet, basename='records')

urlpatterns = [
    path('', include(router.urls)),
]

