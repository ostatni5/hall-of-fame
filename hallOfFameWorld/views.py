from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from HallOfFame.permissions import isStudent, isLecturer, isAdmin


class WorldView(TemplateView):
    template_name = "hallOfFameWorld/world.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if isStudent(request.user):
                return redirect("/student/")
            if isLecturer(request.user):
                return redirect("/lecturer/")
            if isAdmin(request.user):
                return redirect("/admin/")
        return super().get(request, args, kwargs)

