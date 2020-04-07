from django.contrib import admin

# Register your models here.
from hallOfFameClient.models import Subject, Lecturer, Group, Student, Score

admin.site.register(Score)
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Lecturer)
admin.site.register(Subject)