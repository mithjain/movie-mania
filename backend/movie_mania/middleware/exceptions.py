import traceback

from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, ParseError, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from django.conf import settings


def process_validation_error(detail):
    if isinstance(detail, dict):
        message = ''
        for key, value in detail.items():
            if key == 'non_field_errors':
                message = value[0]
            else:
                temp = ''
                for items in value:
                    temp = temp + items + ' '
                    message = message + '{}: {}'.format(key, temp)

        return message
    return detail


def drf_exception_handler(exc, context):
    """
    Custom Exception handler for DRF calls for this app
    :param exc: Exception raised
    :param context: Context of the exception
    :return: Proper Error Response
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    _movie_exceptions = (

    )
    # Now add the HTTP status code to the response.
    if isinstance(exc, ValidationError):
        if isinstance(exc.detail, dict):
            message = process_validation_error(exc.detail)
            response.status_code = 400
            response.data['message'] = message
        elif isinstance(exc.detail, list):
            response.status_code = 400
            response.data = {'message': process_validation_error(exc.detail[0])}

        return response

    elif isinstance(
            exc,
            _movie_exceptions
    ):
        try:
            if exc.params is None:
                if exc.status is None:
                    response = Response(
                        data={'message': exc.message, 'params': exc.params},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                else:
                    response = Response(data={'message': exc.message, 'params': exc.params}, status=exc.status)
                return response
            else:
                if exc.params.get('type') == 'client':
                    if exc.status is None:
                        response = Response(
                            data={'message': exc.message, 'params': exc.params},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
                    else:
                        response = Response(data={'message': exc.message, 'params': exc.params}, status=exc.status)
                else:
                    if exc.status is None:
                        response = Response(
                            data={'message': exc.message, 'params': exc.params},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
                    else:
                        response = Response(data={'message': exc.message, 'params': exc.params}, status=exc.status)
                return response

        except (KeyError, TypeError) as e:
            response = Response(
                data={
                    'message': f"Some internal error occurred. {e}",
                    'params': {
                        'info': f'Internal error while raising the exception. {e}',
                        'type': "server"
                    }
                },
                status=500
            )
            return response

    elif isinstance(exc, AuthenticationFailed):
        try:
            return Response(
                data={
                    'message': str(exc),
                    'params': {
                        'info': str(exc),
                        'type': 'client'
                    }
                },
                status=exc.status_code
            )
        except (KeyError, TypeError) as e:
            response = Response(
                data={
                    'message': f"Some internal error occurred while raising the custom exception. {e}",
                    'params': {
                        'info': str(e),
                        'type': 'server'
                    }
                },
                status=500
            )
            return response

    elif isinstance(exc, ParseError):
        return Response(
            data={'message': str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # if nothing else, then send the response at least. Do not break on 500
    else:
        if settings.DEBUG:
            traceback.print_exc()
        return Response(
            data={'message': str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
