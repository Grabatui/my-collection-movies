from dependency_injector import containers, providers
from dependency_injector.ext import flask
from flask import Flask
from flask_restful import Api

from app.core.domain.search.provider import Provider
from app.core.useCase.search import SearchUseCase
from app.core.persistence.repository import Database, CacheMoviesRepository
from app.core.persistence.action.search import SaveSearchInCache
from app.core.persistence.model.search import CacheMovieModel


class Container(containers.DeclarativeContainer):
    app = flask.Application(Flask, __name__)
    apiV1 = flask.Extension(Api)

    configuration = providers.Configuration()


    database = providers.Factory(
        Database,
        database_string=configuration.database_string
    )
    cacheMoviesRepository = providers.Factory(
        CacheMoviesRepository,
        database=database
    )


    searchCacheMoviesModel = providers.Singleton(CacheMovieModel)


    searchProvider = providers.Factory(
        Provider,
        kinopoisk_token=configuration.kinopoisk_token
    )
    searchSaveSearchInCache = providers.Factory(
        SaveSearchInCache,
        cacheMoviesRepository=cacheMoviesRepository,
        cacheMoviesModel=searchCacheMoviesModel
    )

    searchUseCase = providers.Factory(
        SearchUseCase,
        provider=searchProvider,
        saveSearchInCache=searchSaveSearchInCache
    )
