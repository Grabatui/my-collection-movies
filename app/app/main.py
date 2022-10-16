import os

from .core.di.container import Container


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

app = container.app()


from .core.presentation import v1

if __name__ == '__main__':
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)
