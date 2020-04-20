from django.contrib import admin

# Register your models here.
from hallOfFameClient.models import Subject, Lecturer, Group, Student, StudentScore, Semester, Exercise

admin.site.register(StudentScore)
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Lecturer)
admin.site.register(Subject)
admin.site.register(Exercise)
admin.site.register(Semester)
