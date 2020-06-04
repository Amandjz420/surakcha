from marshmallow import Schema as BaseSchema


class Schema(BaseSchema):
    """
    Base Schema Class. All API Schemas
    are supposed to inherit from this class.

    This class is supposed to provide any changes or
    additions to base marshmallow schema.
    """
    pass

__all__ = ['Schema']
