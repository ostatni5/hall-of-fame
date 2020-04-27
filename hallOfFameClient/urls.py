from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from .admin import lecturer_admin_site
from .views import MyView, TabView, StatView
from .views import SubjectListView

app_name = 'hallOfFameClient'
urlpatterns = [
    path('mine/', MyView.as_view(), name='my-view'),
    path('tab/', TabView.as_view(), name='tab-view'),
    path('stat/', StatView.as_view(), name='stat-view'),
    path('subjects/', SubjectListView.as_view(), name='subject-list'),

]
