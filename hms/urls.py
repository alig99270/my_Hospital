from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Swagger/OpenAPI configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Hospital Management System API",
        default_version='v1',
        description="API documentation for HMS",
        terms_of_service="https://example.com/policies/terms/ ",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # JWT Authentication Endpoints
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Include app-specific URLs under /api/
    path('api/', include('accounts.urls')),
    path('api/', include('shifts.urls')),
    path('api/', include('appointments.urls')),
    path('api/', include('medical_records.urls')),
    path('api/', include('prescriptions.urls')),
    path('api/', include('audit.urls')),
    # Reporting & Statistics
    path('api/', include('reporting.urls')),
    # Notifications & SMS
    path('api/', include('notifications.urls')),
    # Dashboard
    path('api/', include('dashboard.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
