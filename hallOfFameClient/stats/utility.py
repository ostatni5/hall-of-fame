import json
from datetime import datetime

from django.core import serializers
from django.db.models import Sum, Q, F, Avg

from hallOfFameClient.models import Subject, Student, Group, StudentScore, StatGroupScore, StatGroupStudentScore, \
    StatSubjectScore, StatSubjectStudentScore, ArchiveRecord, Variable

Student.objects.values('pk', 'groups__pk', 'groups__stat_score__max_score').annotate(score=Sum('scores__value'), )

Group.objects.values('pk', ).annotate(max_score=Sum('exercises__max_score'))

Group.objects.values('pk', ).annotate(core=Sum('exercises__scores__value'))

StudentScore.objects.values('exercise__group__pk').annotate(score=Sum('value'))


def calcStatsSubject():
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

    arch_record = ArchiveRecord()
    arch_record.save()
    jsonDate = arch_record.creation_date.strftime('%Y-%m-%d %H:%M')
    # last_stats = Variable.objects.get_or_create(key="last_stats", defaults={"value": jsonDate})
    last_date = datetime.strptime(jsonDate, '%Y-%m-%d %H:%M')
    print(last_date)


def rankingSubject(subject_pk):
    return StatSubjectStudentScore.objects.filter(subject__pk=subject_pk).order_by('-mean_value')


def rankingGroup(group_pk):
    return StatGroupStudentScore.objects.filter(stat_group__group__pk=group_pk).order_by('-mean_value')
