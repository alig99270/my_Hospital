from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DoctorProfileViewSet, PatientProfileViewSet, RegisterViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet,basename='users')
router.register(r'doctors', DoctorProfileViewSet,basename='doctors')
router.register(r'patients', PatientProfileViewSet,basename='patients')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterViewSet.as_view({'post': 'create'}), name='register'),  # Manual registration endpoint
]