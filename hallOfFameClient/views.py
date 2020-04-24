import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View, generic
from django.views.generic.list import ListView

from hallOfFameClient.db_manager import getFullGroupData
from hallOfFameClient.models import Subject, Group


class MyView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello world")


class TabView(View):
    template_name = 'hallOfFameClient/tab.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'subject': Subject.objects.first()})


class SubjectListView(ListView):
    model = Subject

    # paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = "Michał Krawczyk"
        return context
