from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, SMSLogViewSet, NotificationTemplateViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)
router.register(r'sms-logs', SMSLogViewSet)
router.register(r'templates', NotificationTemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
