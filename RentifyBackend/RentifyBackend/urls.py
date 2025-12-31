from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser

schema_view = get_schema_view(
    openapi.Info(
        title="Rentify APIs",
        default_version='v1',
        description="API documentation for Rentify",
    ),
    public=False,
    authentication_classes=[SessionAuthentication],
    permission_classes=[IsAdminUser],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/users/', include('users.urls')),
    path('api/vehicles/', include('vehicles.urls')),
    path('api/reservations/', include('reservation.urls')),

    path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
