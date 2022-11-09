from enum import Enum
from typing import Optional
from flask import request
from flask_restx import Resource, fields
from flask_restx.fields import Raw
from dependency_injector.wiring import Provide, inject
import functools

from app.main import app
from app.core.useCase.common import ValidateAccessTokenUseCase
from app.core.di.container import Container


marshal_error_fields = {
    'error': fields.String,
    'fields': fields.Raw
}


class ResultEnum(Enum):
    success = 'success'
    error = 'error'


class ResultField(Raw):
    def format(self, value):
        return value.value if isinstance(value, ResultEnum) else ResultEnum.error.value


class AbstractResource(Resource):
    def _send_error(
        self,
        message: str,
        additionalData: Optional[dict] = None,
        status: int = 500
    ) -> tuple:
        data = additionalData if additionalData is not None else {}

        data['error'] = message

        return {
            'status': ResultEnum.error,
            'data': data
        }, status

    def _send_form_error(
        self,
        errors: dict,
        status: int = 500
    ) -> tuple:
        return self._send_error(
            'Form is invalid',
            additionalData={'fields': errors},
            status=status
        )


class AuthorizationTokenIsInvalid(Exception):
    pass


def jwt_required(function):
    @functools.wraps(function)
    @inject
    def wrapper(
        self,
        validateAccessTokenUseCase: ValidateAccessTokenUseCase = Provide[Container.validateAccessToken],
        *args,
        **kwargs
    ):
        authorization = request.headers.get('Authorization')

        if not authorization or type(authorization) is not str:
            raise AuthorizationTokenIsInvalid('Authorization is required')

        try:
            _, accessToken = authorization.split(' ')
        except:
            raise AuthorizationTokenIsInvalid('Access token is invalid')

        try:
            validateAccessTokenUseCase.run(accessToken)
        except Exception as exception:
            raise AuthorizationTokenIsInvalid(str(exception))

        return function(self, *args, **kwargs)

    return wrapper
        

