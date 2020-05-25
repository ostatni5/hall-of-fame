from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from .admin import lecturer_admin_site
from .views import LecturerGroupTabView, DashboardLecturerView,StatView

app_name = 'lecturer'
urlpatterns = [
    # path('', DashboardLecturerView.as_view(), name='dashboard')
    # path('hallOfFameClient/subject/<int:pk>')
]

