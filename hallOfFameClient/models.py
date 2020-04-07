from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from hallOfFameClient.validators import validate_album_number, RelationValidator


class Student(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    album_number = models.IntegerField(validators=[validate_album_number])

    def __str__(self):
        return self.nickname


class Lecturer(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    def __str__(self):
        return self.name + " " + self.surname


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50)
    students = models.ManyToManyField(Student, related_name="groups")
    lecturers = models.ManyToManyField(Lecturer, related_name="groups")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def has_student(self, student_pk):
        return self.students.get(pk=student_pk).exist()

    def __str__(self):
        return self.name


@deconstructible
class IsInGroupValidator(RelationValidator):
    message = _('Ensure this student in group %(obj_name).')
    code = 'in_group'

    def checkRelation(self, a, b):
        self.obj_name = Group.objects.all().get(pk=b).name
        return not Student.objects.all().filter(pk=a).groups.filter(pk=b).exist()


class Score(models.Model):
    value = models.IntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                validators=[IsInGroupValidator(primary_key=group.pk)])
    date = models.DateTimeField(default=timezone.now)

    

    def __str__(self):
        return self.value.__str__()
