import os

from .core.di.container import Container


def create_app():
    container = Container()
    container.configuration.kinopoisk_token.from_env('KINOPOISK_TOKEN', required=True, as_=str)
    container.configuration.database_string.from_value(
        'postgresql+pg8000://{user}:{password}@{host}/{database}'.format(
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            database=os.environ['DB_DATABASE']
        )
    )
    container.configuration.auth_url.from_env('AUTH_URL')

    app = container.app()
    app.config['ERROR_INCLUDE_MESSAGE'] = False

    container.configuration.root_path.from_value(
        os.path.dirname(app.instance_path)
    )

    app.container = container

    return app


def init_routes():
    from .core.presentation import v1

app = create_app()
init_routes()
