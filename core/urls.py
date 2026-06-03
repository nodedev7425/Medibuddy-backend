"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.views import LoginView
from api.forms import LoginForm

from api.views import ScheduleConfigApiView, AlertApiView, UserAlertApiView
from core.views import devices, device_detail, box_detail, schedule_create, schedule_delete

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name="registration/login.html",
        authentication_form=LoginForm
    ), name='login'),

    path('', devices, name='devices'),

    path(
        'device/<uuid:device_id>/',
        device_detail,
        name='device-detail'
    ),

    path(
        'device/<uuid:device_id>/box/<uuid:box_id>/',
        box_detail,
        name='box-detail'
    ),

    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    path('api/config', ScheduleConfigApiView.as_view(), name='api-config'),
    path('api/alert', AlertApiView.as_view(), name='api-alert'),
    path('api/alert/me', UserAlertApiView.as_view(), name='api-alert-me'),

    path('device/<uuid:device_id>/box/<uuid:box_id>/', box_detail, name='box-detail'),
    path('device/<uuid:device_id>/box/<uuid:box_id>/schedule/create/', schedule_create, name='schedule-create'),
    path('device/<uuid:device_id>/box/<uuid:box_id>/schedule/<uuid:schedule_id>/delete/', schedule_delete, name='schedule-delete'),
]
