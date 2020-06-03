def is_in_group(user, group):
    return user.groups.filter(name=group).exists()


def is_admin(user):
    return is_in_group(user, "admins")


def is_lecturer(user):
    return is_in_group(user, "lecturers")


def is_student(user):
    return is_in_group(user, "students")


def can_access_subject(user, subject_pk):
    return user.lecturer.subjects.filter(pk=subject_pk).exists()


def can_access_group(user, group_pk):
    return user.lecturer.groups.filter(pk=group_pk).exists()


def can_insert_score(user, exercise):
    return exercise.group.lecturers.filter(pk=user.lecturer.pk).exists()


def can_update_score(user, score):
    return can_insert_score(user, score.exercise)
