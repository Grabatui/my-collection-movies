from app.main import container, app


api = container.apiV1()
api.prefix = '/v1'


from . import search


container.wire(modules=[search])

api.add_resource(search.Search, '/search')

api.init_app(app)
