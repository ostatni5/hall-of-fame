from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from hallOfFameClient.models import Student, Subject, StudentScore, Exercise, StatSubjectStudentScore, Group

color = "primary"
user_type = "student"


class RankingStudentView(TemplateView):

    """ ------------------------------TUTAJ SZYMON TO MI DAJ------------------------------- """
    student = Student.objects.filter(album_number=213700).first()   #Aktualny user
    compare_groups = []                                             #Grupy Usera
    compare_my_averages = []                                        #Moje średnie w grupach
    compare_group_averages = []                                     #Średnie tych grup

    def get_context_data(self, **kwargs):
        return "DETALE BITCH!"
    """
    Potrzeba:   <-- do tego trzeba ogarnąć Chart.js albo coś podobnego, więc to można później
        User,
        Wykres słubkowy
                Lista grup Usera,
                Średnia w danej grupie
                Średnia z przedmiotu ogólna
    """


class GroupStudentView(TemplateView):
    template_name = 'hallOfFameStudent/group_student.html'

    """ ------------------------------TUTAJ SZYMON TO MI DAJ------------------------------- """
    student = Student.objects.filter(album_number=213700).first()   #Aktualny user
    checked_exercises = StudentScore.objects.all()                  #Oceny za zadania w grupie
    pending_exercises = Exercise.objects.all()                      #Nieocenione zadania
    group_ranking = Student.objects.all()                           #Lista osób z grupy
                                                                    # + ewentualnie rangi
    my_average = StatSubjectStudentScore.objects.filter(student=student). \
        aggregate(avg=Avg('mean_value'))['avg']                     #Moja średnia w grupie
    my_ranking = 15                                                 #Pozycja egzekwo w rankingu

    cos_do_wykresu_zmiany_rangi_w_czasie_ale_nie_wiem_w_jakiej_formie = 2137

    student = Student.objects.filter(album_number=213700).first()
    group_students = Student.objects.all()
    group_exercises = Exercise.objects.all()

    def get_context_data(self, **kwargs):
        group = get_object_or_404(Group, id=self.kwargs.get('course_id', None))
        context = super().get_context_data(**kwargs)
        context['username'] = self.student.name + " " + self.student.surname
        context['subject'] = group.subject
        context['my_average'] = self.my_average
        context['my_ranking'] = self.my_ranking
        context['group_students'] = self.group_ranking
        context['group_exercises'] = self.checked_exercises
        context['user_type'] = user_type
        context['primary_color'] = color
        return context

    """
    Potrzeba:
        Dane do wykresu RANKING W CZASIE <-- do tego trzeba ogarnąć Chart.js albo coś podobnego, więc to można później
                kolejność w rankingu po danym zadaniu
                średnia po danym zadaniu
    """


class DashboardStudentView(TemplateView):
    template_name = 'hallOfFameStudent/dashboard_student.html'

    """ ------------------------------TUTAJ SZYMON TO MI DAJ--------------------------------------- """
    student = Student.objects.filter(album_number=213700).first()   #Aktualny user
    scores = StudentScore.objects.order_by('-date')[:12][::-1]       #Ostatnie N ocen
    groups = Group.objects.all()                                    #MojeGrupy
    my_average = 88                                                 #Moja średnia z całości
    semester_average = 76                                           #Średnia z całości
    total_ETCS = 30                                                 #Suma punktów z kursów

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.student.name + " " + self.student.surname
        context['averages'] = {
            'my_average': self.my_average,
            'semester_average': self.semester_average
        }
        context['courses'] = self.groups
        context['total_ETCS'] = self.total_ETCS
        context['score_diagram'] = {
            'label': [],
            'percentage': [],
            'score': [],
            'max_score': [],
            'date': [],
            'subject': [],
        }
        context['user_type'] = user_type
        context['primary_color'] = color
        for score in self.scores:
            context['score_diagram']['label'].append('Exercise: ' + score.exercise.name)
            context['score_diagram']['percentage'].append((score.value*100.0)/score.exercise.max_score)
            context['score_diagram']['score'].append(score.value)
            context['score_diagram']['max_score'].append(score.exercise.max_score)
            context['score_diagram']['date'].append(score.date)
            context['score_diagram']['subject'].append(score.exercise.group.subject.name)
        return context


class LoginStudentView(TemplateView):
    template_name = 'hallOfFameStudent/login_student.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = user_type
        context['primary_color'] = color
        return context
