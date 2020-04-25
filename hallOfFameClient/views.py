from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic.list import ListView

from hallOfFameClient.models import Subject


class MyView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')

class SubjectListView(ListView):

    model = Subject
    # paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = "Michał Krawczyk"
        context['diagramUrl'] = "https://media.discordapp.net/attachments/689977881535053839/701202475906236456/unknown.png"
        context['myAverage'] = "88"
        context['semesterAverage'] = "76"
        return context