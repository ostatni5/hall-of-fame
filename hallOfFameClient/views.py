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
        return context