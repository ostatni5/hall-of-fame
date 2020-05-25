import json

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic.list import ListView

from hallOfFameClient.models import StudentScore, Exercise

from hallOfFameClient.models import Subject, Student, Lecturer, Group
from HallOfFame.permissions import isLecturer, canAccessSubject, canUpdateScore, canInsertScore, canAccessGroup
from hallOfFameClient.stats.utility import calc_all_stats


class UserLecturerTestMixinView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/lecturer/login/'

    def test_func(self):
        flag = True
        user = self.request.user
        flag = flag and isLecturer(user)
        return flag


class LecturerGroupTabView(UserLecturerTestMixinView):
    template_name = 'hallOfFameClient/group_tab.html'

    def test_func(self):
        user = self.request.user
        subject = Subject.objects.filter(pk=self.kwargs['pk']).first()
        if subject is None:
            return False
        return super().test_func() and canAccessSubject(user, subject.pk) and canAccessGroup(user,
                                                                                             self.kwargs['group_pk'])

    def get_ctx(self):
        subject = Subject.objects.get(pk=self.kwargs['pk'])

        groups = subject.groups.filter(pk=self.kwargs['group_pk']).all()

        groups_ctx = {}
        for group in groups:
            groups_ctx[group.pk] = {}
            groups_ctx[group.pk]["name"] = group.name
            groups_ctx[group.pk]["pk"] = group.pk
            groups_ctx[group.pk]["scores"] = {}

            exercises = group.exercises.all()
            students = group.students.all()
            groups_ctx[group.pk]["exercises"] = exercises.values()
            groups_ctx[group.pk]["students"] = students.values()

            groups_ctx[group.pk]["scores"]["sum"] = {}
            for student in group.students.all():
                groups_ctx[group.pk]["scores"][student.pk] = {}
                groups_ctx[group.pk]["scores"]["sum"][student.pk] = 0

            groups_ctx[group.pk]["max_score"] = 0
            for exercise in exercises:
                groups_ctx[group.pk]["max_score"] += exercise.max_score
                for score in exercise.scores.all():
                    groups_ctx[group.pk]["scores"][score.student.pk][score.exercise.pk] = model_to_dict(score)
                    groups_ctx[group.pk]["scores"]["sum"][score.student.pk] += score.value
        return subject, groups_ctx

    def parse_score_name(self, score, value):
        (n, pk, s_id, e_id) = score.split('-')
        if value == '':
            value = 0
        return {"id": pk, "student": s_id, "exercise": e_id, "value": value}

    def filter_request(self, request):
        update_scores = []
        create_scores = []
        print(request.POST["change_info"])
        change_info = json.loads(request.POST["change_info"])
        for req, value in request.POST.items():
            if req[0:3] == "ss-" and change_info.get(req):
                if req[3:5] == "{}":
                    create_scores.append(self.parse_score_name(req, value))
                else:
                    update_scores.append(self.parse_score_name(req, value))
        return update_scores, create_scores

    def post(self, request, *args, **kwargs):
        update_scores, create_scores = self.filter_request(request)
        saved_scores = 0

        for score in update_scores:
            q = StudentScore.objects.get(pk=score["id"])
            if canUpdateScore(request.user, q):
                q.value = score.get("value")
                q.date = timezone.now()
                q.save()

                saved_scores += 1

        for score in create_scores:
            student = Student.objects.get(pk=score.get("student"))
            exercise = Exercise.objects.get(pk=score.get("exercise"))
            if canInsertScore(request.user, exercise):
                StudentScore.objects.create(student=student, exercise=exercise,
                                            value=score.get("value"))
                saved_scores += 1

        if saved_scores > 0:
            calc_all_stats(force=True, to_archive=False)

        msg = "Saved {0} scores".format(saved_scores)
        subject, groups_ctx = self.get_ctx()
        return render(request, self.template_name,
                      {'groupsCtx': groups_ctx, "subject": subject, "msg": msg})

    def get(self, request, *args, **kwargs):
        subject, groups_ctx = self.get_ctx()
        return render(request, self.template_name,
                      {'groupsCtx': groups_ctx, "subject": subject})


class StatView(View):
    template_name = 'hallOfFameClient/stat.html'
    stat = StudentScore.objects.values("exercise__group__subject", "exercise__group", "exercise", ).annotate(
        sum_value=Sum('value'),
        sum_max_score=Sum('exercise__max_score'))

    stat2 = StudentScore.objects.values("student", "exercise__group__subject", "exercise__group", ).annotate(
        sum_value=Sum('value'),
        sum_max_score=Sum('exercise__max_score'))

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {"stat": self.stat, "stat2": self.stat2})


class DashboardLecturerView(UserLecturerTestMixinView, View):
    template_name = 'hallOfFameClient/dashboard_lecturer.html'

    # paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        lecturer = self.request.user.lecturer
        context = {}
        context['lecturer'] = lecturer
        context['username'] = lecturer.name + " " + lecturer.surname
        context['subjects'] = lecturer.subjects.all()
        context['groups'] = lecturer.groups.all()
        context[
            'diagramUrl'] = "https://media.discordapp.net/attachments/689977881535053839/701202475906236456/unknown.png"

        groups_by_sub = {}
        for g in context['groups']:
            if g.subject.pk in groups_by_sub:
                groups_by_sub[g.subject.pk].append(g)
            else:
                groups_by_sub[g.subject.pk] = [g]

        context['groups_by_sub'] = groups_by_sub
        print(context)
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


"""
Potrzeba:
    User (Prowadzący),
    Lista przedmiotów w których jest prowadzącym
            Nazwa przedmiotu
            Opis krótki
            Lista grup w których prowadzi ten przedmiot
                nazwa grupy
                ilość osób
"""
