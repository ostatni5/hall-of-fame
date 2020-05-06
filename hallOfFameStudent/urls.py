from django.urls import path

from hallOfFameStudent.views import DashboardStudentView, GroupStudentView

app_name = 'student'
urlpatterns = [
    path('', DashboardStudentView.as_view(), name='dashboard'),
    path('subject/<int:sub_id>', GroupStudentView.as_view(), name='subject')
]