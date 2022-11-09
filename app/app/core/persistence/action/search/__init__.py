from typing import List

from app.core.domain.search import SaveSearchHistoryInterface, SaveSearchInCacheInterface
from app.core.domain.search.entity import SearchFilter, ResponseMovie, SearchMovie
from app.core.persistence.repository import SearchHistoryRepository, CacheMoviesRepository
from app.core.persistence.model.search import SearchHistoryModel, SearchMovieModel


class SaveSearchHistoryAction(SaveSearchHistoryInterface):
    def __init__(
        self,
        searchHistoryRepository: SearchHistoryRepository,
        searchHistoryModel: SearchHistoryModel
    ) -> None:
        self.searchHistoryRepository = searchHistoryRepository
        self.searchHistoryModel = searchHistoryModel

    def run(self, filter: SearchFilter) -> int:
        entity = self.searchHistoryModel.fromQueryToPersistence(
            filter.toDictionary()
        )

        self.searchHistoryRepository.insert(entity)

        return entity.id


class SaveSearchInCacheAction(SaveSearchInCacheInterface):
    def __init__(
        self,
        cacheMoviesRepository: CacheMoviesRepository,
        searchMoviesModel: SearchMovieModel
    ) -> None:
        self.cacheMoviesRepository = cacheMoviesRepository
        self.searchMoviesModel = searchMoviesModel

    def run(self, searchHistoryId: int, items: List[ResponseMovie]) -> List[SearchMovie]:
        persistenceItems = []

        persistenceItems = [self.searchMoviesModel.fromResponseMovieToPersistence(searchHistoryId, responseMovie) for responseMovie in items]

        self.cacheMoviesRepository.insert_many(persistenceItems)

        repositoryIdsToSupplierIds = {}
        for persistenceItem in persistenceItems:
            repositoryIdsToSupplierIds[persistenceItem.external_id] = persistenceItem.id

        returnResult = []
        for responseMovie in items:
            returnResult.append(
                self.searchMoviesModel.fromResponseMovieToSearchMovie(
                    responseMovie,
                    repositoryIdsToSupplierIds[responseMovie.id]
                )
            )

        return returnResult
