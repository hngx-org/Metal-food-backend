from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('users.urls')),
    path('api/v1/transaction/', include('transaction.urls')),
    # YOUR PATTERNS
    # path('api/v1/schema', SpectacularAPIView.as_view(), name='schema'),
    # # Optional UI:
    # path('api/v1/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/v1/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path('api/v1/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]

