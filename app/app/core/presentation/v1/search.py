from flask import request
from flask_restx import marshal_with, fields
from dependency_injector.wiring import Provide, inject
from wtforms import Form as BaseForm, fields as forms_fields, validators

from app.core.presentation.v1.helpers import AbstractResource, ResultEnum, ResultField, marshal_error_fields, jwt_required
from app.core.di.container import Container
from app.core.domain.search.entity import SearchFilter
from app.core.useCase.search import SearchUseCase


class Form(BaseForm):
    title = forms_fields.StringField('Title', [validators.Length(min=2)])
    year = forms_fields.IntegerField('Year')



class Search(AbstractResource):
    data = marshal_error_fields.copy()
    data.update({
        'items': fields.List(
            fields.Nested(
                {
                    'id': fields.Integer,
                    'titles': fields.List(
                        fields.Nested({
                            'language': fields.String(attribute='language.name'),
                            'value': fields.String
                        })
                    ),
                    'year': fields.Integer,
                    'rating': fields.Float
                },
                allow_null=True,
                skip_none=True
            )
        )
    })
    resource_fields = {
        'status': ResultField,
        'data': fields.Nested(data, skip_none=True)
    }

    @jwt_required
    @inject
    @marshal_with(fields=resource_fields, skip_none=True)
    def post(self, searchUseCase: SearchUseCase = Provide[Container.searchUseCase]):
        form = Form(data=request.get_json())
        if not form.validate():
            return self._send_form_error(form.errors, status=400)

        items = searchUseCase.get(
            SearchFilter(
                title=form.title.data,
                year=form.year.data
            )
        )

        return {
            'status': ResultEnum.success,
            'data': {'items': items}
        }
