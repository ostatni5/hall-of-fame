from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


def validate_album_number(value):
    if value < 100000 or value > 999999:
        raise ValidationError(
            _('%(value)s is not an album number'),
            params={'value': value},
        )


@deconstructible
class RelationValidator:
    message = _('Ensure this field is in relation %(primary_key) with %(obj_name).')
    code = 'primary_key'

    def __init__(self, primary_key, message=None):
        self.primary_key = primary_key
        self.obj_name = ''
        if message:
            self.message = message

    def __call__(self, value):
        cleaned = self.clean(value)
        primary_key = self.primary_key() if callable(self.primary_key) else self.primary_key
        params = {'primary_key': primary_key, 'obj_name': self.obj_name, 'value': value}
        if self.checkRelation(cleaned, primary_key):
            raise ValidationError(self.message, code=self.code, params=params)

    def __eq__(self, other):
        return (
                isinstance(other, self.__class__) and
                self.limit_value == other.limit_value and
                self.message == other.message and
                self.code == other.code
        )

    def checkRelation(self, a, b):
        return a is not b

    def clean(self, x):
        return x
