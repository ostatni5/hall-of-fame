from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from hallOfFameClient.validators import validate_album_number


class Basic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Semester(models.Model):
    number = models.PositiveSmallIntegerField()
    etcs = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.number.__str__()


class Person(Basic):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " " + self.surname

    class Meta:
        abstract = True


class Student(Person):
    nickname = models.CharField(max_length=50, unique=True)
    album_number = models.IntegerField(validators=[validate_album_number], unique=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="students")

    def __str__(self):
        return self.album_number.__str__()


class Lecturer(Person):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)


class Subject(Basic):
    description = models.CharField(max_length=250)
    # long_description = models.CharField(max_length=300)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="subject")
    etcs = models.SmallIntegerField()
    lecturers = models.ManyToManyField(Lecturer, related_name="subjects")


class Group(Basic):
    name = models.CharField(max_length=100, unique=True)
    students = models.ManyToManyField(Student, related_name="groups")
    lecturers = models.ManyToManyField(Lecturer, related_name="groups")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="groups")

    def has_student(self, student_pk):
        return self.students.get(pk=student_pk).exist()


class Exercise(Basic):
    date = models.DateTimeField(default=timezone.now)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="exercises")
    max_score = models.SmallIntegerField()


class StudentScore(models.Model):
    value = models.SmallIntegerField()
    exercise = models.ForeignKey(Exercise,
                                 on_delete=models.CASCADE,
                                 related_name="scores")
    student = models.ForeignKey(Student,
                                on_delete=models.CASCADE,
                                related_name="scores")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.value.__str__()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['exercise', 'student'], name='only one score per exercise for student')
        ]


class StatModel(models.Model):
    mean_value = models.FloatField()

    class Meta:
        abstract = True


class StatGroupScore(StatModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="stat_score")
    max_score = models.SmallIntegerField()


class StatGroupStudentScore(StatModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="stat_groups_score")
    stat_group = models.ForeignKey(StatGroupScore, on_delete=models.CASCADE, related_name="stat_students_score")
    value = models.SmallIntegerField()


class StatSubjectScore(StatModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="stat_score")


class StatSubjectStudentScore(StatModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="stat_subjects_score")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="stat_students_score")


class Variable(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()


class ArchiveRecord(models.Model):
    creation_date = models.DateTimeField()


class ArchiveModel(StatModel):
    mean_value = models.FloatField()

    class Meta:
        abstract = True

class ArchiveSubjectStudentScore(ArchiveModel):
    record = models.ForeignKey(ArchiveRecord, on_delete=models.CASCADE, related_name="subjects_scores")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="arch_subjects_score")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="arch_students_score")

class ArchiveGroupStudentScore(ArchiveModel):
    record = models.ForeignKey(ArchiveRecord, on_delete=models.CASCADE, related_name="students_scores")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="arch_groups_score")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="arch_students_score")
