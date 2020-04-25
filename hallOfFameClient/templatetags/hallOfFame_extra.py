from django import template

register = template.Library()


@register.filter
def scoreSearch(scores, student):
    return scores.get_or_create(student=student, defaults={'value': 0})[0]
