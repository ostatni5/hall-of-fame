from django.contrib import admin
from django.apps import apps
# Register your models here.
from django.contrib.admin import AdminSite
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.auth.models import User
from django.urls import path

from hallOfFameClient.models import Subject, Group, StudentScore, Exercise
from HallOfFame.permissions import isAdmin, isLecturer
from hallOfFameClient.views import DashboardLecturerView, TabView


class ExerciseInLine(admin.TabularInline):
    model = Exercise
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('students', 'lecturers')
    inlines = [
        ExerciseInLine,
    ]

    def get_queryset(self, request):
        if isAdmin(request.user):
            return super().get_queryset(request)
        return request.user.lecturer.groups

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject":
            kwargs["queryset"] = request.user.lecturer.subjects
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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

    def get_queryset(self, request):
        if isAdmin(request.user):
            return super().get_queryset(request)
        return request.user.lecturer.subjects


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

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('', LecturerAdminSite.admin_view(self, DashboardLecturerView.as_view())),
            path('hallOfFameClient/', LecturerAdminSite.admin_view(self, DashboardLecturerView.as_view())),
            path('subject/<int:pk>/scores/', LecturerAdminSite.admin_view(self, TabView.as_view()),
                 name="subject_scores"),
        ]
        return my_urls + urls


lecturer_admin_site = LecturerAdminSite(name='lecturer')
lecturer_admin_site.register(Subject, SubjectAdmin)
lecturer_admin_site.register(Exercise)
lecturer_admin_site.register(Group, GroupAdmin)
# lecturer_admin_site.register(StudentScore)
