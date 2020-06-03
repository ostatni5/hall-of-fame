from django import template
from django.db.models import Sum

register = template.Library()


@register.filter
def score_search(scores, student):
    return scores.get_or_create(student=student, defaults={'value': 0})[0]


@register.filter
def percent_score(scores, group):
    score = list(scores.filter(exercise__group=group).aggregate(total=Sum('value')))[1]
    max_score = list(group.exercises.aggregate(total=Sum('max_score')))[1]
    return score / max_score


@register.filter
def key(h, k):
    try:
        return h[k]
    except KeyError:
        return None


@register.filter
def key_s(h, k):
    # silent
    try:
        return h[k]
    except KeyError:
        return {}


@register.filter
def percent(value, full):
    if full == 0:
        return 100
    return value / full * 100


@register.filter
def round_to(value, prec):
    return round(value, prec)


@register.filter
def data_id(value):
    return "data-{0}".format(value)
