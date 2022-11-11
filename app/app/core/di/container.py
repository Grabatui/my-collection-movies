from dependency_injector import containers, providers
from flask import Flask
from flask_restx import Api

from app.core.domain.common import LoggerProvider
from app.core.domain.search.provider import Provider
from app.core.useCase.common import ValidateAccessTokenUseCase
from app.core.useCase.search import SearchUseCase
from app.core.persistence.repository import Database, SearchHistoryRepository, CacheMoviesRepository, AuthExternalRepository
from app.core.persistence.action.common import IsAccessTokenValidAction
from app.core.persistence.action.search import SaveSearchHistoryAction, SaveSearchInCacheAction
from app.core.persistence.model.search import SearchHistoryModel, SearchMovieModel


class Container(containers.DeclarativeContainer):
    app = providers.Singleton(Flask, __name__)
    apiV1 = providers.Singleton(Api)

    configuration = providers.Configuration()


    database = providers.Singleton(
        Database,
        database_string=configuration.database_string
    )
    searchHistoryRepository = providers.Singleton(
        SearchHistoryRepository,
        database=database
    )
    cacheMoviesRepository = providers.Singleton(
        CacheMoviesRepository,
        database=database
    )
    authExternalRepository = providers.Singleton(
        AuthExternalRepository,
        endpointPrefix=configuration.auth_url
    )


    searchSearchMoviesModel = providers.Singleton(SearchMovieModel)
    searchHistoryModel = providers.Singleton(SearchHistoryModel)


    searchProvider = providers.Singleton(
        Provider,
        kinopoisk_token=configuration.kinopoisk_token
    )
    loggerProvider = providers.Singleton(
        LoggerProvider,
        logRootPath=configuration.root_path
    )


    saveSearchHistory = providers.Singleton(
        SaveSearchHistoryAction,
        searchHistoryRepository=searchHistoryRepository,
        searchHistoryModel=searchHistoryModel
    )
    searchSaveSearchInCache = providers.Singleton(
        SaveSearchInCacheAction,
        cacheMoviesRepository=cacheMoviesRepository,
        searchMoviesModel=searchSearchMoviesModel
    )
    isAccessTokenValidAction = providers.Singleton(
        IsAccessTokenValidAction,
        repository=authExternalRepository
    )

    searchUseCase = providers.Singleton(
        SearchUseCase,
        provider=searchProvider,
        saveSearchHistory=saveSearchHistory,
        saveSearchInCache=searchSaveSearchInCache
    )
    validateAccessToken = providers.Singleton(
        ValidateAccessTokenUseCase,
        isAccessTokenValid=isAccessTokenValidAction,
        loggerProvider=loggerProvider
    )
