from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError as DjangoValidationError


def custom_exception_handler(exc, context):
    """Custom exception handler to format error responses consistently."""
    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {'error': 'An unexpected error occurred', 'detail': str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    error_response = {
        'error': response.data.get('detail', 'Unknown error'),
        'code': response.status_code
    }

    return Response(error_response, status=response.status_code)