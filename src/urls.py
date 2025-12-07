"""
URL configuration for src project.
"""

from django.urls import path
from django.urls import include
from django.contrib import admin
from django.conf.urls.static import static

from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from src.settings.base import STATIC_URL
from src.settings.base import STATIC_ROOT


schema_view = get_schema_view(
    openapi.Info(
        title="Wallet API",
        default_version='v1',
        description="API documentation for Wallet project",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.wallets.routers.urls")),

    # Swagger
    path("swagger(<format>\.json|\.yaml)", schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
