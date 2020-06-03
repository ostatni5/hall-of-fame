from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from HallOfFame.permissions import is_student, is_lecturer, is_admin


class WorldView(TemplateView):
    template_name = "hallOfFameWorld/world.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if is_student(request.user):
                return redirect("/student/")
            if is_lecturer(request.user):
                return redirect("/lecturer/")
            if is_admin(request.user):
                return redirect("/admin/")
        return super().get(request, args, kwargs)

