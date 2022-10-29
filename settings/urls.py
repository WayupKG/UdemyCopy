from django.contrib import admin
from django.urls import path, include

from settings.yasg import urlpatterns as yasg_urlpatterns


api_v1 = [
    path('accounts/', include('apps.user.urls')),
    path('swagger/', include(yasg_urlpatterns)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_v1)),
]
