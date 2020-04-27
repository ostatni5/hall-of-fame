from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
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
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="subject")
    etcs = models.SmallIntegerField()


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
