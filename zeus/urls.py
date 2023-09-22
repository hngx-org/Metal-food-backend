from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import  *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('users.urls')),
    path('api/v1/transaction/', include('transaction.urls')),
    #  YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

