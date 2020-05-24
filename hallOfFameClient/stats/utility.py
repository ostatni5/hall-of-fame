import json
from datetime import datetime

from django.core import serializers
from django.db.models import Sum, Q, F, Avg, QuerySet
from django.utils import timezone

from hallOfFameClient.models import Subject, Student, Group, StudentScore, StatGroupScore, StatGroupStudentScore, \
    StatSubjectScore, StatSubjectStudentScore, ArchiveRecord, Variable, ArchiveSubjectStudentScore, \
    ArchiveGroupStudentScore

Student.objects.values('pk', 'groups__pk', 'groups__stat_score__max_score').annotate(score=Sum('scores__value'), )

Group.objects.values('pk', ).annotate(max_score=Sum('exercises__max_score'))

Group.objects.values('pk', ).annotate(core=Sum('exercises__scores__value'))

StudentScore.objects.values('exercise__group__pk').annotate(score=Sum('value'))


def archStats(curr_date):
    arch_record = ArchiveRecord()
    arch_record.creation_date = curr_date
    arch_record.save()

    query_group = StatGroupStudentScore.objects.all()
    objs = []
    for res in query_group:
        obj = ArchiveGroupStudentScore()
        obj.record = arch_record
        obj.student = res.student
        obj.group = res.stat_group.group
        obj.mean_value = res.mean_value
        objs.append(obj)
    ArchiveGroupStudentScore.objects.bulk_create(objs)

    query_subject = StatSubjectStudentScore.objects.all()
    objs = []
    for res in query_subject:
        obj = ArchiveSubjectStudentScore()
        obj.record = arch_record
        obj.student = res.student
        obj.subject = res.subject
        obj.mean_value = res.mean_value
        objs.append(obj)
    ArchiveSubjectStudentScore.objects.bulk_create(objs)


def calcStatsSubject():
    curr_date = timezone.now()
    last_date = ArchiveRecord.objects.all().order_by('-creation_date').first()

    create = True
    if last_date is not None:
        diff_hours = (curr_date - last_date.creation_date).total_seconds() / 3600
        create = (diff_hours > 24)

    if not create:
        return -1

    StatGroupScore.objects.all().delete()
    StatGroupStudentScore.objects.all().delete()
    StatSubjectScore.objects.all().delete()
    StatSubjectStudentScore.objects.all().delete()

    query_group = Group.objects.values('pk', ).annotate(max_score=Sum('exercises__max_score'))
    objs = []
    for res in query_group:
        obj = StatGroupScore()
        obj.group_id = res['pk']
        obj.max_score = res['max_score'] or 0
        obj.mean_value = 0
        objs.append(obj)
    StatGroupScore.objects.bulk_create(objs)

    query_students = Student.objects.values('pk', 'groups__pk', 'groups__stat_score__pk',
                                            'groups__stat_score__max_score').annotate(score=Sum('scores__value'), )
    objs = []
    for res in query_students:
        obj = StatGroupStudentScore()
        obj.student_id = res['pk']
        obj.stat_group_id = res['groups__stat_score__pk']
        obj.value = res['score']
        val = res['groups__stat_score__max_score']
        obj.mean_value = res['score'] * 100 / val if val != 0 else 0
        objs.append(obj)
    StatGroupStudentScore.objects.bulk_create(objs)

    query_group_avg = StatGroupStudentScore.objects.values('stat_group__pk').annotate(mean_value=Avg('mean_value'), )

    objs = []
    for res in query_group_avg:
        obj = StatGroupScore.objects.get(pk=res['stat_group__pk'])
        obj.mean_value = res['mean_value']
        objs.append(obj)
    StatGroupScore.objects.bulk_update(objs, ['mean_value'])

    query_subject_avg = StatGroupScore.objects.values('group__subject__pk').annotate(mean_value=Avg('mean_value'), )
    objs = []
    for res in query_subject_avg:
        obj = StatSubjectScore()
        obj.subject_id = res['group__subject__pk']
        obj.mean_value = res['mean_value']
        objs.append(obj)
    StatSubjectScore.objects.bulk_create(objs)

    query_subject_student = StatGroupStudentScore \
        .objects.values('student__pk',
                        'stat_group__group__subject__pk') \
        .annotate(mean_value=Avg('mean_value'), )
    objs = []
    for res in query_subject_student:
        obj = StatSubjectStudentScore()
        obj.subject_id = res['stat_group__group__subject__pk']
        obj.student_id = res['student__pk']
        obj.mean_value = res['mean_value']
        objs.append(obj)
    StatSubjectStudentScore.objects.bulk_create(objs)

    archStats(curr_date)


def rankingSubject(subject_pk):
    return StatSubjectStudentScore.objects.filter(subject__pk=subject_pk).order_by('-mean_value')


def rankingGroup(group_pk):
    return StatGroupStudentScore.objects.filter(stat_group__group__pk=group_pk).order_by('-mean_value')


def createRankingStudents(students_desc):
    ranking, my_pos = createRankingStudentsAndMe(students_desc, -1)
    return ranking


def createRankingStudentsAndMe(students_desc, student_pk):
    ranking = []
    my_pos = -1
    pos = 1
    last = 999
    if type(students_desc) is QuerySet:
        last = students_desc.first().mean_value
    else:
        last = students_desc[0].mean_value
    for student in students_desc:
        if student.mean_value < last:
            pos += 1
        student.pos = pos
        if student.student.pk == student_pk:
            my_pos = pos
        ranking.append(student)
    return ranking, my_pos


def splitArchiveRankingStudents(days_students_desc):
    days = [days_students_desc.first().record.creation_date]
    rankings = []
    last_record = days_students_desc.first().record
    ranking = []
    for row in days_students_desc:
        if row.record != last_record:
            rankings.append(ranking)
            days.append(row.record.creation_date)
            ranking = [row]
        else:
            ranking.append(row)
    rankings.append(ranking)
    return rankings, days
