from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

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

    def __str__(self):
        return self.name + " " + self.surname

    class Meta:
        abstract = True


class Student(Person):
    nickname = models.CharField(max_length=50)
    album_number = models.IntegerField(validators=[validate_album_number])
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname


class Lecturer(Person):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)


class Subject(Basic):
    description = models.CharField(max_length=250)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    etcs = models.SmallIntegerField()


class Group(Basic):
    students = models.ManyToManyField(Student, related_name="groups")
    lecturers = models.ManyToManyField(Lecturer, related_name="groups")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def has_student(self, student_pk):
        return self.students.get(pk=student_pk).exist()


class Exercise(Basic):
    date = models.DateTimeField(default=timezone.now)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    max_score = models.SmallIntegerField()


class StudentScore(models.Model):
    value = models.SmallIntegerField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.value.__str__()
