from dependency_injector import containers, providers
from dependency_injector.ext import flask
from flask import Flask
from flask_restful import Api

from app.core.domain.search.provider import Provider
from app.core.useCase.search import SearchUseCase


class Container(containers.DeclarativeContainer):
    app = flask.Application(Flask, __name__)
    apiV1 = flask.Extension(Api)

    configuration = providers.Configuration()


    searchProvider = providers.Factory(
        Provider,
        kinopoisk_token=configuration.kinopoisk_token
    )

    searchUseCase = providers.Factory(
        SearchUseCase,
        provider=searchProvider
    )
