from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import logout
from django.shortcuts import redirect

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path(r'api/', include('wallet.urls')),
    path('admin/', admin.site.urls),
]
