from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from hallOfFameClient.models import Student, Subject, StudentScore
from polls.views import DetailView


class RankingStudentView(DetailView):
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
    model = Subject

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.student.name + " " + self.student.surname
        context[
            'diagramUrl'] = "https://media.discordapp.net/attachments/689977881535053839/701202475906236456/unknown.png"
        context['myAverage'] = "88"
        context['semesterAverage'] = "76"
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
    """
