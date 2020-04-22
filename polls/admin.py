from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Question, Choice

admin.site.register(Question)
admin.site.register(Choice)


