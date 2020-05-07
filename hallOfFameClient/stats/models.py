from django.db import models
from django.db.models import Sum
from django.utils import timezone

from hallOfFameClient.models import Student, Group, Subject


class StatModel(models.Model):
    date = models.DateTimeField(default=timezone.now)
    mean_value = models.FloatField()

    class Meta:
        abstract = True


class StatGroupStudentScore(StatModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="stat_groups_score")
    stat_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="stat_students_score")
    value = models.SmallIntegerField()


class StatGroupScore(StatModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="stat_score")
    max_score = models.SmallIntegerField()

    def calc(self, group):
        pass


class StatSubjectScore(StatModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="stat_score")


