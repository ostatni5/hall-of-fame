def isInGroup(user, group):
    return user.groups.filter(name=group).exists()


def isAdmin(user):
    return isInGroup(user, "admins")


def isLecturer(user):
    return isInGroup(user, "lecturers")


def isStudent(user):
    return isInGroup(user, "students")


def canAccessSubject(user, subject_pk):
    return user.lecturer.subjects.filter(pk=subject_pk).exists()


def canAccessGroup(user, group_pk):
    return user.lecturer.groups.filter(pk=group_pk).exists()


def canInsertScore(user, exercise):
    return exercise.group.lecturers.filter(pk=user.lecturer.pk).exists()


def canUpdateScore(user, score):
    return canInsertScore(user, score.exercise)
