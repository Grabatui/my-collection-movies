from dependency_injector import containers, providers
from flask import Flask
from flask_restx import Api

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


    database = providers.Factory(
        Database,
        database_string=configuration.database_string
    )
    searchHistoryRepository = providers.Factory(
        SearchHistoryRepository,
        database=database
    )
    cacheMoviesRepository = providers.Factory(
        CacheMoviesRepository,
        database=database
    )
    authExternalRepository = providers.Factory(
        AuthExternalRepository,
        endpointPrefix=configuration.auth_url
    )


    searchSearchMoviesModel = providers.Singleton(SearchMovieModel)
    searchHistoryModel = providers.Singleton(SearchHistoryModel)


    searchProvider = providers.Factory(
        Provider,
        kinopoisk_token=configuration.kinopoisk_token
    )
    saveSearchHistory = providers.Factory(
        SaveSearchHistoryAction,
        searchHistoryRepository=searchHistoryRepository,
        searchHistoryModel=searchHistoryModel
    )
    searchSaveSearchInCache = providers.Factory(
        SaveSearchInCacheAction,
        cacheMoviesRepository=cacheMoviesRepository,
        searchMoviesModel=searchSearchMoviesModel
    )
    isAccessTokenValidAction = providers.Factory(
        IsAccessTokenValidAction,
        repository=authExternalRepository
    )

    searchUseCase = providers.Factory(
        SearchUseCase,
        provider=searchProvider,
        saveSearchHistory=saveSearchHistory,
        saveSearchInCache=searchSaveSearchInCache
    )
    validateAccessToken = providers.Factory(
        ValidateAccessTokenUseCase,
        isAccessTokenValid=isAccessTokenValidAction,
        logRootPath=configuration.root_path
    )
