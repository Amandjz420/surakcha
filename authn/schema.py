from marshmallow import post_load, validates

from elapi.base_schema import Schema
from elapi.fields import fields
from elapi.exceptions import InvalidDataException
from .authn_helper import valid_mobile_number, create_otp


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
    def create_otp(self, data, **kwargs):
        data['otp'] = create_otp()
        return data


class OTPSchema(Schema):
    """
    OTP Verification API Schema
    """
    mobile = fields.Number(required=True)
    otp = fields.Number(required=True)

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
