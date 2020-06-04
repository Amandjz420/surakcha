from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom Exception handler to format the response
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Add status and nest exceptions data under errors
    if response is not None:
        resp = {'status': 400, 'errors': response.data}
        response.data = resp

    return response


__all__ = ['custom_exception_handler']
