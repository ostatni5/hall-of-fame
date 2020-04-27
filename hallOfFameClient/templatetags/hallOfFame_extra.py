from django import template
from django.db.models import Sum

register = template.Library()


@register.filter
def scoreSearch(scores, student):
    return scores.get_or_create(student=student, defaults={'value': 0})[0]


@register.filter
def percentScore(scores, group):
    score = list(scores.filter(exercise__group=group).aggregate(total=Sum('value')))[1]
    max_score = list(group.exercises.aggregate(total=Sum('max_score')))[1]
    return score / max_score


@register.filter
def key(h, k):
    return h[k]


@register.filter
def percent(value, full):
    if full == 0:
        return 100
    return value / full * 100
