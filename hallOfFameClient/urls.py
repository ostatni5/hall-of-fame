from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from .admin import lecturer_admin_site

app_name = 'hallOfFameClient'
urlpatterns = [
    path('lecturer/', lecturer_admin_site.urls),
]