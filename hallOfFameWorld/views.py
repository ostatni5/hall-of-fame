from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class WorldView(TemplateView):
    template_name = "hallOfFameWorld/world.html"
