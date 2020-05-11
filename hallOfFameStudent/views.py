from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import View

from hallOfFameClient.models import Student, Subject, StudentScore, Exercise, StatSubjectStudentScore
from polls.views import DetailView

color = "primary"
user_type = "student"


class RankingStudentView(TemplateView):
    def get_context_data(self, **kwargs):
        return "DETALE BITCH!"

    """
    Potrzeba:   <-- do tego trzeba ogarnąć Chart.js albo coś podobnego, więc to można później
        User,
        Wykres słubkowy
                Lista grup Usera,
                Średnia w danej grupie
                Średnia z przedmiotu ogólna
        Lista rankingu osób w Roczniku
                User
                Średnia całkowita
                Miejsce w rankingu (egzekwo mają to samo miejsce)
        Dane do wykresu RANKING W CZASIE 
                kolejność w rankingu w danym miesiącu
                średnia pw danym miesiącu
    """


class GroupStudentView(TemplateView):
    template_name = 'hallOfFameClient/group_student.html'
    student = Student.objects.filter(album_number=213700).first()
    # model = StudentScore
    group_students = Student.objects.all()
    group_exercises = Exercise.objects.all()

    def get_context_data(self, **kwargs):
        student = self.student
        context = super().get_context_data(**kwargs)
        context['username'] = self.student.name + " " + self.student.surname
        context['subject'] = get_object_or_404(Subject, id=self.kwargs.get('sub_id', None))
        context['myaverage'] = "88"#StatSubjectStudentScore.objects.filter(student=student). \
            #agreggate(avg=Avg('mean_value'))['avg']
        context['myranking'] = "15"
        context['groupstudents'] = self.group_students
        context['groupexercises'] = self.group_exercises
        context['usertype'] = user_type
        context['primaryColor'] = color
        return context

    """
    Potrzeba:
        User,
        Grupa o id 'sub_id', <-- nazwę zmienię potem, bo teraz to jest id przedmiotu, ale zmieni się to 
        Twoja średnia w grupie (z przedmiotu), 
        Twój ranking (egzekwo mają to samo miejsce)
        Lista ocen z zadań na zajęciach
                wszystkie dane z zadania
                ocena
                procentowo
        Lista rankingu osób w grupie
                User
                Średnia
                Miejsce w rankingu (egzekwo mają to samo miejsce)
        Dane do wykresu RANKING W CZASIE <-- do tego trzeba ogarnąć Chart.js albo coś podobnego, więc to można później
                kolejność w rankingu po danym zadaniu
                średnia po danym zadaniu
    """


class DashboardStudentView(ListView):
    template_name = 'hallOfFameClient/dashboard_student.html'
    student = Student.objects.filter(album_number=213700).first()
    scores = StudentScore.objects.order_by('-date')[:5]
    model = Subject

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.student.name + " " + self.student.surname
        context['myAverage'] = "88"
        context['semesterAverage'] = "76"
        context['diagramLabel'] = []
        context['diagramData'] = []
        context['userType'] = user_type
        context['primaryColor'] = color
        for score in self.scores:
            context['diagramLabel'].append(score.exercise.name)
            context['diagramData'].append(score.value)
        return context

    """
    Potrzeba:
        User,
        Średnia Usera (całkowita),
        Średnia wszystkich na roku (całkowita),
        Dane do wykresu <- to się później ustali
        Lista grup w których ma zajęcia
                Nazwa przedmiotu grupy
                Nazwa grupy
                opis krótki
                ECTS
    """


class LoginStudentView(TemplateView):
    template_name = 'hallOfFameClient/login_student.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userType'] = user_type
        context['primaryColor'] = color
        return context
