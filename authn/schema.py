from marshmallow import post_load, validates

from elapi.base_schema import Schema
from elapi.fields import fields
from elapi.exceptions import InvalidDataException
from .authn_helper import valid_mobile_number, create_otp
from .models import User


class LoginSchema(Schema):
    """
    User API Schema
    """
    name = fields.String(required=True)
    mobile = fields.Number(required=True)

    @validates("mobile")
    def validates_mobile(self, value):
        if not valid_mobile_number(value):
            raise InvalidDataException("Not a valid mobile Number")

    @post_load
    def post_processing(self, data, **kwargs):
        data['otp'] = create_otp()
        data['existing_user'] = not User.objects.filter(mobile=data['mobile']).exists()
        return data


class OTPSchema(Schema):
    """
    OTP Verification API Schema
    """
    mobile = fields.Number(required=True)
    otp = fields.Number(required=True)
    gender = fields.String(required=False, allow_none=True)
    email = fields.String(required=False, allow_none=True)

    # @validates_schema
    # def validates_payload_data(self, data):
    #     if not valid_mobile_number(data['mobile']):
    #         raise InvalidDataException("Not a valid mobile Number")
    #     if data['otp'] < 100000 or data['otp'] > 100000:
    #         raise InvalidDataException("invalid OTP")
    #     return data


class TokenSchema(Schema):
    """
    OTP Verification API Schema
    """
    token = fields.Number(required=True, read_only=True)
