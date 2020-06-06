from marshmallow import post_load, validates

from elapi.base_schema import Schema
from elapi.fields import fields
from elapi.exceptions import InvalidDataException


class PublicTokenApiSchema(Schema):
    """
    User API Schema
    """
    public_token = fields.String(required=True)


class TransactionSchema(Schema):
    """
    Transaction Schema
    """
    mobile = fields.Number(required=True)
    otp = fields.Number(required=True)
    gender = fields.String(required=False, allow_none=True)
    email = fields.String(required=False, allow_none=True)


# class TokenSchema(Schema):
#     """
#     OTP Verification API Schema
#     """
#     token = fields.Number(required=True, read_only=True)
