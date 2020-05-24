from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg, Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
import random

from HallOfFame.permissions import isStudent
from hallOfFameClient.models import Student, Subject, StudentScore, Exercise, StatSubjectStudentScore, Group, \
    StatGroupStudentScore, ArchiveGroupStudentScore
from hallOfFameClient.stats.utility import create_ranking_students, create_ranking_students_and_me, \
    split_archive_ranking_students

color = "primary"
user_type = "student"


class StudentView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/student/login/'

    def test_func(self):
        flag = True
        user = self.request.user
        return flag and isStudent(user)

    def handle_no_permission(self):
        return redirect('student:login')


class RankingStudentView(StudentView, TemplateView):
    """ ------------------------------TUTAJ SZYMON TO MI DAJ------------------------------- """

    def get_context_data(self, **kwargs):
        student = self.request.user.student  # Aktualny user
        compare_groups = []  # Grupy Usera
        compare_my_averages = []  # Moje średnie w grupach
        compare_group_averages = []  # Średnie tych grup
        return "DETALE BITCH!"

    """
    Potrzeba:   <-- do tego trzeba ogarnąć Chart.js albo coś podobnego, więc to można później
        User,
        Wykres słubkowy
                Lista grup Usera,
                Średnia w danej grupie
                Średnia z przedmiotu ogólna
    """


class GroupStudentView(StudentView, TemplateView):
    template_name = 'hallOfFameStudent/group_student.html'

    def get_context_data(self, **kwargs):
        student = self.request.user.student
        group = get_object_or_404(Group, id=self.kwargs.get('course_id', None))
        checked_exercises = student.scores.filter(exercise__group=group)
        # niechleuj -------------------------------------------------------
        pending_exercises = group.exercises.difference(group.exercises.filter(scores__student=student))
        group_students = StatGroupStudentScore.objects.filter(stat_group__group=group).order_by('-mean_value').all()
        group_ranking, my_ranking = create_ranking_students_and_me(group_students, student.pk)  # obj.pos

        my_average = checked_exercises.aggregate(avg=Avg('value'))['avg']

        cos_do_wykresu_zmiany_rangi_w_czasie_ale_nie_wiem_w_jakiej_formie = 2137

        arch_group_students = ArchiveGroupStudentScore.objects.filter(group=group).order_by('-record__creation_date',
                                                                                            '-mean_value').all()

        arch_group_students_s, days = split_archive_ranking_students(arch_group_students)
        arch_group_ranking, arch_my_ranking = ([], [])
        for arch_group in arch_group_students_s:
            ranking, my = create_ranking_students_and_me(arch_group, student.pk)
            arch_group_ranking.append(ranking)
            arch_my_ranking.append(my)
        arch_group_ranking[0] = group_ranking
        arch_my_ranking[0] = my_ranking
        context = super().get_context_data(**kwargs)
        context['username'] = student.name + " " + student.surname
        context['subject'] = group.subject
        context['name'] = group.name
        context['my_ranking'] = {
            'position': my_ranking,
            'average': my_average
        }
        context['group_ranking'] = {
            'student_ranking': []
        }
        if(len(arch_group_ranking) < 2):
            for ranking in group_ranking:
                context['group_ranking']['student_ranking'].append(ranking)
                context['group_ranking'][ranking.student.pk] = 0;
        else:
            for i in range(len(group_ranking)):
                ranking = group_ranking[i]
                last_ranking_pos = ranking.pos
                if(len(arch_group_ranking[1])>i):
                    last_ranking_pos = arch_group_ranking[1][i].pos
                context['group_ranking']['student_ranking'].append(ranking)
                context['group_ranking'][ranking.student.pk] = last_ranking_pos - ranking.pos

        context['exercises'] = {
            'pending': pending_exercises,
            'checked': checked_exercises
        }

        for obj in group_ranking:
            print(obj)

        context['user_type'] = user_type
        context['primary_color'] = color
        return context


"""
Potrzeba:
    Dane do wykresu RANKING W CZASIE <-- do tego trzeba ogarnąć Chart.js albo coś podobnego, więc to można później
            kolejność w rankingu po danym zadaniu
            średnia po danym zadaniu
"""


class DashboardStudentView(StudentView, TemplateView):
    template_name = 'hallOfFameStudent/dashboard_student.html'

    def get_context_data(self, **kwargs):
        student = self.request.user.student
        scores = student.scores.all().order_by('-date')[:5][::-1]
        groups = student.groups.all()
        my_average = StatSubjectStudentScore.objects.filter(student=student).aggregate(avg=Avg('mean_value'))['avg']
        semester_average = StatSubjectStudentScore.objects.aggregate(avg=Avg('mean_value'))['avg']
        total_ETCS = student.groups.values('subject').distinct().aggregate(etcs=Sum('subject__etcs'))['etcs']

        context = super().get_context_data(**kwargs)
        context['username'] = student.name + " " + student.surname
        context['averages'] = {
            'my_average': my_average,
            'semester_average': semester_average
        }
        context['courses'] = groups
        context['total_ETCS'] = total_ETCS
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
        for score in scores:
            context['score_diagram']['label'].append('Exercise: ' + score.exercise.name)
            context['score_diagram']['percentage'].append((score.value * 100.0) / score.exercise.max_score)
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

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if isStudent(request.user):
                return redirect('/student/')
            context = self.get_context_data()
            context["error"] = """You are authorised not as a student. Please login student account."""
            return render(request, self.template_name, context)
        return super().get(request, *args, **kwargs)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/student/')
        else:
            context = self.get_context_data()
            context["error"] = """Please enter the correct username and password."""
            return render(request, self.template_name, context)


class LogoutStudentView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect('student:login')
