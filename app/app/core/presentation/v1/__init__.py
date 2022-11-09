from app.main import app
from .helpers import AuthorizationTokenIsInvalid, ResultEnum


api = app.container.apiV1()
api.prefix = '/v1'


from . import search


app.container.wire(modules=[search])

api.add_resource(search.Search, '/search')

api.init_app(app)


@api.errorhandler(AuthorizationTokenIsInvalid)
def handle_token_is_invalid(exception):
    return {
        'status': ResultEnum.error.value,
        'data': {'error': str(exception)}
    }, 401
