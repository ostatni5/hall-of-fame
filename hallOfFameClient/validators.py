from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


def validate_album_number(value):
    if value < 100000 or value > 999999:
        raise ValidationError(
            _('%(value)s is not an album number'),
            params={'value': value},
        )


