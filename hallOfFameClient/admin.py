from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite

from hallOfFameClient.models import Subject, Lecturer, Group, Student, StudentScore, Semester, Exercise


class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('students', 'lecturers')








class LecturerAdminSite(AdminSite):
    site_header = 'Monty Python administration'

    def has_permission(self, request):
        """
        Removed check for is_staff.
        """
        return request.user.is_active


lecturer_admin_site = LecturerAdminSite(name='lectureradminsite')

lecturer_admin_site.register(Subject)
lecturer_admin_site.register(Exercise)
lecturer_admin_site.register(Group, GroupAdmin)


# admin.site.register(Group, GroupAdmin)
# admin.site.register(StudentScore)
# admin.site.register(Student)
# admin.site.register(Lecturer)
# admin.site.register(Subject)
# admin.site.register(Exercise)
# admin.site.register(Semester)
