from django.db.models import Sum, Avg, QuerySet
from django.utils import timezone

from hallOfFameClient.models import Student, Group, StudentScore, StatGroupScore, StatGroupStudentScore, \
    StatSubjectScore, StatSubjectStudentScore, ArchiveRecord, ArchiveSubjectStudentScore, \
    ArchiveGroupStudentScore

Student.objects.values('pk', 'groups__pk', 'groups__stat_score__max_score').annotate(score=Sum('scores__value'), )
Group.objects.values('pk', ).annotate(max_score=Sum('exercises__max_score'))
Group.objects.values('pk', ).annotate(core=Sum('exercises__scores__value'))
StudentScore.objects.values('exercise__group__pk').annotate(score=Sum('value'))


# -------------archive
def arch_group_student(query_group, arch_record):
    objs = []
    for res in query_group:
        obj = ArchiveGroupStudentScore()
        obj.record = arch_record
        obj.student = res.student
        obj.group = res.stat_group.group
        obj.mean_value = res.mean_value
        objs.append(obj)
    return objs


def arch_subject_student(query_subject, arch_record):
    objs = []
    for res in query_subject:
        obj = ArchiveSubjectStudentScore()
        obj.record = arch_record
        obj.student = res.student
        obj.subject = res.subject
        obj.mean_value = res.mean_value
        objs.append(obj)
    return objs


def arch_stats(curr_date):
    arch_record = ArchiveRecord()
    arch_record.creation_date = curr_date
    arch_record.save()

    query_group = StatGroupStudentScore.objects.all()
    objs = arch_group_student(query_group, arch_record)
    ArchiveGroupStudentScore.objects.bulk_create(objs)

    query_subject = StatSubjectStudentScore.objects.all()
    objs = arch_subject_student(query_subject, arch_record)
    ArchiveSubjectStudentScore.objects.bulk_create(objs)


# -------------stats
def clear_all_stats():
    StatGroupScore.objects.all().delete()
    StatGroupStudentScore.objects.all().delete()
    StatSubjectScore.objects.all().delete()
    StatSubjectStudentScore.objects.all().delete()


def calc_max_score_group(query_group):
    objs = []
    for res in query_group:
        obj = StatGroupScore()
        obj.group_id = res['pk']
        obj.max_score = res['max_score'] or 0
        obj.mean_value = 0
        objs.append(obj)
    return objs


def calc_student_score_group(query_students):
    objs = []
    for res in query_students:
        obj = StatGroupStudentScore()
        obj.student_id = res['student__pk']
        obj.stat_group_id = res['exercise__group__stat_score__pk']
        obj.value = res['score']
        val = res['exercise__group__stat_score__max_score']
        obj.mean_value = res['score'] * 100 / val if val != 0 else 0
        objs.append(obj)
    return objs


def calc_avg_group(query_group_avg):
    objs = []
    for res in query_group_avg:
        obj = StatGroupScore.objects.get(pk=res['stat_group__pk'])
        obj.mean_value = res['mean_value']
        objs.append(obj)
    return objs


def calc_avg_subject(query_subject_avg):
    objs = []
    for res in query_subject_avg:
        obj = StatSubjectScore()
        obj.subject_id = res['group__subject__pk']
        obj.mean_value = res['mean_value']
        objs.append(obj)
    return objs

def calc_subject_student(query_subject_student):
    objs = []
    for res in query_subject_student:
        obj = StatSubjectStudentScore()
        obj.subject_id = res['stat_group__group__subject__pk']
        obj.student_id = res['student__pk']
        obj.mean_value = res['mean_value']
        objs.append(obj)
    return objs


def calc_all_stats(force, to_archive):
    curr_date = timezone.now()
    last_date = ArchiveRecord.objects.all().order_by('-creation_date').first()

    create = True
    if last_date is not None:
        diff_hours = (curr_date - last_date.creation_date).total_seconds() / 3600
        create = (diff_hours > 24)

    if not create and not force:
        return -1

    clear_all_stats()

    query_group = Group.objects.values('pk', ).annotate(max_score=Sum('exercises__max_score'))
    objs = calc_max_score_group(query_group)
    StatGroupScore.objects.bulk_create(objs)

    query_students = StudentScore.objects.values("student__pk", 'exercise__group__pk',
                                                 'exercise__group__stat_score__pk',
                                                 'exercise__group__stat_score__max_score').annotate(score=Sum('value'))
    objs = calc_student_score_group(query_students)
    StatGroupStudentScore.objects.bulk_create(objs)

    query_group_avg = StatGroupStudentScore.objects.values('stat_group__pk').annotate(mean_value=Avg('mean_value'), )
    objs = calc_avg_group(query_group_avg)
    StatGroupScore.objects.bulk_update(objs, ['mean_value'])

    query_subject_avg = StatGroupScore.objects.values('group__subject__pk').annotate(mean_value=Avg('mean_value'), )
    objs = calc_avg_subject(query_subject_avg)
    StatSubjectScore.objects.bulk_create(objs)

    query_subject_student = StatGroupStudentScore \
        .objects.values('student__pk',
                        'stat_group__group__subject__pk').annotate(mean_value=Avg('mean_value'),)
    objs = calc_subject_student(query_subject_student)
    StatSubjectStudentScore.objects.bulk_create(objs)

    if to_archive:
        arch_stats(curr_date)


# ---------------rankings
def ranking_subject(subject_pk):
    return StatSubjectStudentScore.objects.filter(subject__pk=subject_pk).order_by('-mean_value')


def ranking_group(group_pk):
    return StatGroupStudentScore.objects.filter(stat_group__group__pk=group_pk).order_by('-mean_value')


def create_ranking_students(students_desc):
    ranking, my_pos, my_mean, student_ranking = create_ranking_students_and_me(students_desc, -1)
    return ranking


def create_ranking_students_and_me(students_desc, student_pk):
    ranking = []
    my_pos = -1
    pos = 1
    last = 9999
    my_mean = 0
    student_ranking = {}
    if type(students_desc) is QuerySet:
        if students_desc.first():
            last = students_desc.first().mean_value
    else:
        if len(students_desc) > 0:
            last = students_desc[0].mean_value
    for row in students_desc:
        if round(row.mean_value, 2) < round(last, 2):
            pos += 1
            last = round(row.mean_value, 2)
        row.pos = pos
        student_ranking[row.student.pk] = {"pos": pos, "mean_value": round(row.mean_value, 2),
                                           "name": row.student.name, "surname": row.student.surname,
                                           }
        if row.student.pk == student_pk:
            my_pos = pos
            my_mean = row.mean_value
        ranking.append(row)
    return ranking, my_pos, my_mean, student_ranking


def split_arch_ranking_students(days_students_desc):
    if days_students_desc.first() is None:
        return [], []
    days = [days_students_desc.first().record.creation_date]
    rankings = []
    last_record = days_students_desc.first().record
    ranking = []
    for row in days_students_desc:
        if row.record != last_record:
            rankings.append(ranking)
            days.append(row.record.creation_date)
            ranking = [row]
            last_record = row.record
        else:
            ranking.append(row)
    rankings.append(ranking)
    return rankings, days


def rankings_from_arch_group(arch_group_students_s, student):
    arch_group_ranking, arch_my_ranking, arch_all_ranking = ([], [], [])
    for arch_group in arch_group_students_s:
        ranking, my_pos, mean, student_ranking = create_ranking_students_and_me(arch_group, student.pk)

        arch_group_ranking.append(ranking)
        arch_my_ranking.append(my_pos)
        arch_all_ranking.append(student_ranking)
    return arch_all_ranking, arch_group_ranking, arch_my_ranking