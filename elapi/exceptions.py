from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework import status
from marshmallow.exceptions import ValidationError


EXCEPTION_CODES = {
    'missing': 'E001',  # Missing Required Data in Payload
    'invalid': 'E002',  # Invalid Data Type sent in Payload
    'wrong_data': 'E003',  # Wrong structure or logic problem
    'data_not_found': 'E004',  # Data/object not found in DB
    'duplicate_data': 'E005',  # Duplicate Data
    'db': 'E006',  # DB Exception
    'authorization': 'E007',
    'user_error': 'E008',
}


# Validation Exceptions, 400 errors
class APIOValidationException(RestValidationError):
    """
    Base Exception class
    """
    def __init__(self, message, field='_all', *args, **kwargs):
        message = {field: [{'message': message, 'code': self.code}]}
        super(APIOValidationException, self).__init__(message, *args, **kwargs)


class MissingDataException(APIOValidationException):
    """
    Exception to be raised when data is missing
    in the payload
    """
    code = EXCEPTION_CODES['missing']


class InvalidDataException(APIOValidationException):
    """
    Invalid data type Exception
    """
    code = EXCEPTION_CODES['invalid']


class DataNotFoundException(APIOValidationException):
    """
    Data/Object not found
    """
    code = EXCEPTION_CODES['data_not_found']


class DuplicateDataException(APIOValidationException):
    """
    Duplicate record for unique field
    """
    code = EXCEPTION_CODES['duplicate_data']


class WrongDataException(APIOValidationException):
    """
    Wrong data format sent in request
    """
    code = EXCEPTION_CODES['wrong_data']


class DatabaseException(APIOValidationException):
    """
    Database Exception other that Integrity Error
    """
    code = EXCEPTION_CODES['db']


# Authentication Exceptions, 401 errors
class AuthenticationFailed(APIOValidationException):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = EXCEPTION_CODES['authorization']


class UserException(APIOValidationException):
    """
    When user do wrong process we throw this exception
    """
    code = EXCEPTION_CODES['user_error']


# Schema Exceptions, uses Marshmallow ValidationError Class
class BaseSchemaException(ValidationError):
    """
    Base Validation Error class
    """
    def __init__(self, message, *args, **kwargs):
        message = [{'message': message, 'code': self.code}]
        super(BaseSchemaException, self).__init__(message, *args, **kwargs)


class MissingDataError(BaseSchemaException):
    """
    Exception to be raised when data is missing
    in the payload
    """
    code = EXCEPTION_CODES['missing']


class WrongDataError(BaseSchemaException):
    """
    Exception to be raised when wrong data is passed
    in the payload
    """
    code = EXCEPTION_CODES['wrong_data']


class DataNotFoundError(BaseSchemaException):
    """
    Data/Object not found Error
    """
    code = EXCEPTION_CODES['data_not_found']


__all__ = [
            'EXCEPTION_CODES', 'DataNotFoundError', 'WrongDataError', 'MissingDataError', 'BaseSchemaException',
            'UserException', 'AuthenticationFailed',
            'DatabaseException', 'WrongDataException', 'DuplicateDataException', 'DataNotFoundException',
            'InvalidDataException', 'MissingDataException', 'APIOValidationException',
           ]
