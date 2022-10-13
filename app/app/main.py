from .core.di.container import Container


container = Container()
container.configuration.kinopoisk_token.from_env('KINOPOISK_TOKEN', required=True, as_=str)

app = container.app()


from .core.presentation import v1

if __name__ == '__main__':
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)
