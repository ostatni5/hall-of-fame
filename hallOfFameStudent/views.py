from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from hallOfFameClient.models import Student, Subject, StudentScore


class GroupStudentView(ListView):
    # sub_id = sub_id
    template_name = 'hallOfFameClient/group_student.html'
    student = Student.objects.filter(album_number=213700).first()
    # subject = Subject.objects.filter(name_exact="Elementy statycznego podrywu").first()
    model = StudentScore
    groupStudents = Student.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.student.name + " " + self.student.surname
        context['subject'] = get_object_or_404(Subject, id=self.kwargs.get('sub_id', None))
        context['myAverage'] = "88"
        context['myRanking'] = "15"
        context['groupStudents'] = self.groupStudents
        return context


class DashboardStudentView(ListView):
    template_name = 'hallOfFameClient/dashboard_student.html'
    student = Student.objects.filter(album_number=213700).first()
    model = Subject

    # paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.student.name + " " + self.student.surname
        context[
            'diagramUrl'] = "https://media.discordapp.net/attachments/689977881535053839/701202475906236456/unknown.png"
        context['myAverage'] = "88"
        context['semesterAverage'] = "76"
        return context
