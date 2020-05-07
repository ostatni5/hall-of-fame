from django.db.models import Sum

from hallOfFameClient.models import Subject


def calcStats():
    Subject.objects.values('pk', 'groups').annotate(max_score=Sum('groups__exercises__max_score'))