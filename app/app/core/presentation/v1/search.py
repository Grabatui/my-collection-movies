from typing import List
from flask_restful import Resource, marshal_with, reqparse, fields
from dependency_injector.wiring import Provide, inject

from app.core.di.container import Container
from app.core.domain.search.entity import SearchFilter
from app.core.useCase.search import SearchUseCase


parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
parser.add_argument('year', type=int)


resource_fields = {
    'id': fields.Integer,
    'titles': fields.List(
        fields.Nested({
            'language': fields.String,
            'value': fields.String
        })
    ),
    'year': fields.Integer,
    'rating': fields.Float
}


class Search(Resource):
    @inject
    @marshal_with(fields=resource_fields, envelope='items')
    def post(self, searchUseCase: SearchUseCase = Provide[Container.searchUseCase]):
        arguments = parser.parse_args()

        return searchUseCase.get(
            SearchFilter(
                title=arguments['title'],
                year=arguments['year']
            )
        )
