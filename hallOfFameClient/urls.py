from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from .admin import lecturer_admin_site
from .views import TabView, DashboardStudentView, DashboardLecturerView,StatView

app_name = 'hallOfFameClient'
urlpatterns = [
    path('tab/', TabView.as_view(), name='tab-view'),
    path('dashboard/', DashboardStudentView.as_view(), name='dashboard-student'),
    path('lecturer/', DashboardLecturerView.as_view(), name='dashboard-lecturer'),
    path('stat/', StatView.as_view(), name='stat-view'),
]
