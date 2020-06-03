from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg, Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from HallOfFame.permissions import is_student
from hallOfFameClient.models import StatSubjectStudentScore, Group, \
    StatGroupStudentScore, ArchiveGroupStudentScore
from hallOfFameClient.stats.utility import create_ranking_students_and_me, \
    split_arch_ranking_students, rankings_from_arch_group

user_type = "student"


class StudentView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/student/login/'

    def test_func(self):
        flag = True
        user = self.request.user
        return flag and is_student(user)

    def handle_no_permission(self):
        return redirect('student:login')


class GroupStudentView(StudentView, TemplateView):
    template_name = 'hallOfFameStudent/group_student.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_history'] = True
        context['show_ranking'] = True

        student = self.request.user.student
        group = get_object_or_404(Group, id=self.kwargs.get('course_id', None))

        checked_exercises = student.scores.filter(exercise__group=group)
        pending_exercises = group.exercises.difference(
            group.exercises.filter(scores__student=student))

        group_students = StatGroupStudentScore.objects.filter(stat_group__group=group).order_by('-mean_value').all()
        group_ranking, my_ranking, my_average, all_ranking = create_ranking_students_and_me(group_students,
                                                                                            student.pk)

        arch_group_students = ArchiveGroupStudentScore.objects.filter(group=group).order_by('-record__creation_date',
                                                                                            '-mean_value').all()
        arch_group_students_s, days = split_arch_ranking_students(arch_group_students)
        arch_all_ranking, arch_group_ranking, arch_my_ranking = rankings_from_arch_group(arch_group_students_s,
                                                                                         student)

        if my_ranking == -1:
            if len(arch_group_ranking) > 0:
                group_ranking = arch_group_ranking[0]
                my_ranking = arch_my_ranking[0]
            context['show_history'] = False
            context['show_ranking'] = False
        else:
            days.insert(0, timezone.now())
            arch_group_ranking.insert(0, group_ranking)
            arch_my_ranking.insert(0, my_ranking)
            arch_all_ranking.insert(0, {})

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
        context['chart_data'] = {
            'days': days[1:],
            'rankings': arch_all_ranking[1:],
            'important': student.pk,
        }

        if len(arch_group_ranking) < 2:
            for ranking in group_ranking:
                context['group_ranking']['student_ranking'].append(ranking)
                context['group_ranking'][ranking.student.pk] = 0
        else:

            for last_pos in arch_group_ranking[1]:
                context['group_ranking'][last_pos.student.pk] = last_pos.pos

            for ranking in group_ranking:
                context['group_ranking']['student_ranking'].append(ranking)
                try:
                    context['group_ranking'][ranking.student.pk] -= ranking.pos
                except KeyError:
                    context['group_ranking'][ranking.student.pk] = 0

        context['exercises'] = {
            'pending': pending_exercises,
            'checked': checked_exercises
        }

        context['user_type'] = user_type
        return context


class DashboardStudentView(StudentView, TemplateView):
    template_name = 'hallOfFameStudent/dashboard_student.html'

    def get_context_data(self, **kwargs):
        student = self.request.user.student
        
        scores = student.scores.all().order_by('-date')[:5][::-1]
        my_average = StatSubjectStudentScore.objects.filter(student=student).aggregate(avg=Avg('mean_value'))['avg']
        semester_average = StatSubjectStudentScore.objects.aggregate(avg=Avg('mean_value'))['avg']
        total_ETCS = student.groups.values('subject').distinct().aggregate(etcs=Sum('subject__etcs'))['etcs']

        context = super().get_context_data(**kwargs)
        context['username'] = student.name + " " + student.surname
        context['averages'] = {
            'my_average': my_average,
            'semester_average': semester_average
        }
        context['courses'] = student.groups.all()
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
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if is_student(request.user):
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
