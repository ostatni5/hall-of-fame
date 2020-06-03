from django.contrib import admin
# Register your models here.
from django.contrib.admin import AdminSite
from django.urls import path

from HallOfFame.permissions import is_admin, is_lecturer
from hallOfFameClient.models import Subject, Group, Exercise
from hallOfFameClient.views import DashboardLecturerView, LecturerGroupTabView


class ExerciseInLine(admin.TabularInline):
    model = Exercise
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('students', 'lecturers')
    inlines = [
        ExerciseInLine,
    ]

    def get_queryset(self, request):
        if is_admin(request.user):
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
        if is_admin(request.user):
            return super().get_queryset(request)
        return request.user.lecturer.subjects


class LecturerAdminSite(AdminSite):
    site_header = "LecturerAdminSite"
    site_title = "LecturerAdminSite Portal"
    index_title = "Welcome to LecturerAdminSite Portal"

    def has_permission(self, request):
        flag = False
        if not request.user.is_anonymous:
            flag = is_lecturer(request.user)
        return super().has_permission(request) and flag

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('', LecturerAdminSite.admin_view(self, DashboardLecturerView.as_view()), name="dashboard"),
            path('hallOfFameClient/', LecturerAdminSite.admin_view(self, DashboardLecturerView.as_view()),
                 name="client"),
            path('subject/<int:pk>/scores/<int:group_pk>',
                 LecturerAdminSite.admin_view(self, LecturerGroupTabView.as_view()),
                 name="subject_scores"),
        ]
        return my_urls + urls


lecturer_admin_site = LecturerAdminSite(name='lecturer')
lecturer_admin_site.register(Subject, SubjectAdmin)
lecturer_admin_site.register(Exercise)
lecturer_admin_site.register(Group, GroupAdmin)
