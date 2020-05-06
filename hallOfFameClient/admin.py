from django.contrib import admin
from django.apps import apps
# Register your models here.
from django.contrib.admin import AdminSite
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.auth.models import User

from hallOfFameClient.models import Subject, Lecturer, Group, Student, StudentScore, Semester, Exercise
from hallOfFameClient.permissions import isAdmin, isLecturer


class ExerciseInLine(admin.TabularInline):
    model = Exercise
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('students', 'lecturers')
    inlines = [
        ExerciseInLine,
    ]


class GroupInline(admin.StackedInline):
    filter_horizontal = ('students', 'lecturers')
    model = Group
    extra = 1

    class Media:
        css = {
            'all': ('admin/edit_inline/stacked.css',)
        }


class SubjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('lecturers',)
    inlines = [
        GroupInline,
    ]


class LecturerAdminSite(AdminSite):
    site_header = "LecturerAdminSite"
    site_title = "LecturerAdminSite Portal"
    index_title = "Welcome to LecturerAdminSite Portal"

    def has_permission(self, request):
        flag = False
        if not request.user.is_anonymous:
            flag = isLecturer(request.user)
            flag = flag or request.user.is_superuser
        return super().has_permission(request) and flag


lecturer_admin_site = LecturerAdminSite(name='lecturer')
lecturer_admin_site.register(Subject, SubjectAdmin)
lecturer_admin_site.register(Exercise)
lecturer_admin_site.register(Group, GroupAdmin)
lecturer_admin_site.register(StudentScore)


class DefaultAdminSite(AdminSite):
    site_header = "DefaultAdminSite"
    site_title = "DefaultAdminSite Portal"
    index_title = "Welcome to DefaultAdminSite Portal"

    def has_permission(self, request):
        flag = False
        if not request.user.is_anonymous:
            flag = isAdmin(request.user)
            flag = flag or request.user.is_superuser
        return super().has_permission(request) and flag


default_admin_site = DefaultAdminSite(name='admin')

models = apps.get_app_config('hallOfFameClient').get_models()

default_admin_site.register(User)

for model in models:
    try:
        default_admin_site.register(model)
    except AlreadyRegistered:
        pass
