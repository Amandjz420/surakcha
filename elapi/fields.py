from django.forms.fields import MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple

from marshmallow import fields
from marshmallow.utils import missing as missing_
from marshmallow import utils

from .exceptions import EXCEPTION_CODES


class CheckboxMultipleChoiceField(MultipleChoiceField):
    widget = CheckboxSelectMultiple


class BaseMixin(object):
    """
    Base Field Mixin to override error message format and mark
    fields as required by default
    """
    default_error_messages = {
        'required': [{'message': 'Missing data for required field', 'code': EXCEPTION_CODES['missing']}],
        'null': [{'message': 'Field may not be null', 'code': EXCEPTION_CODES['missing']}],
        'type': [{'message': 'Invalid input type', 'code': EXCEPTION_CODES['invalid']}],
        'invalid': [{'message': 'Invalid input type', 'code': EXCEPTION_CODES['invalid']}],
        'validator_failed': [{'message': 'Invalid value', 'code': EXCEPTION_CODES['invalid']}],
    }

    def __init__(self, *args, **kwargs):
        if 'required' not in kwargs:
            kwargs['required'] = True
        super(BaseMixin, self).__init__(*args, **kwargs)

    def _validate_missing(self, value):
        """Validate missing values. Raise a :exc:`ValidationError` if
        `value` should be considered missing.
        """
        if value is missing_:
            if hasattr(self, 'required') and self.required:
                self.fail('required')
        if value is None or (type(value) == unicode and len(value) == 0):
            if hasattr(self, 'allow_none') and self.allow_none is not True:
                self.fail('null')


class String(BaseMixin, fields.String):
    def _deserialize(self, value, attr, data):
        try:
            value = str(value)
        except:
            pass

        if not isinstance(value, basestring):
            self.fail('invalid')
        return utils.ensure_text_type(value)


class Dict(BaseMixin, fields.Dict):
    def __init__(self, *args, **kwargs):
        super(Dict, self).__init__(*args, **kwargs)
        self.default_error_messages['type'] = [{
            'message': 'Invalid input type. Expected Json Object',
            'code': EXCEPTION_CODES['invalid']}]


class Integer(BaseMixin, fields.Integer):
    pass


class Float(BaseMixin, fields.Float):
    pass


class DateTime(BaseMixin, fields.DateTime):
    pass


class Date(BaseMixin, fields.Date):
    pass


class Boolean(BaseMixin, fields.Boolean):
    pass


class Nested(BaseMixin, fields.Nested):
    pass


class List(BaseMixin, fields.List):
    pass


class Method(BaseMixin, fields.Method):
    pass


class Email(BaseMixin, fields.Email):
    pass


__all__ = [
            'Method', 'List', 'Nested', 'Boolean', 'Date', 'DateTime', 'Float',
            'Integer', 'Dict', 'String', 'ChoiceArrayField', 'CheckboxMultipleChoiceField',
            'Email',
          ]
