from typing import List
import copy

from app.core.domain.search import SaveSearchInCacheInterface
from app.core.domain.search.entity import ResponseMovie, SearchMovie
from app.core.persistence.repository import CacheMoviesRepository
from app.core.persistence.model.search import CacheMovieModel


class SaveSearchInCache(SaveSearchInCacheInterface):
    def __init__(
        self,
        cacheMoviesRepository: CacheMoviesRepository,
        cacheMoviesModel: CacheMovieModel
    ) -> None:
        self.cacheMoviesRepository = cacheMoviesRepository
        self.cacheMoviesModel = cacheMoviesModel

    def run(self, items: List[ResponseMovie]) -> List[SearchMovie]:
        persistenceItems = []

        persistenceItems = [self.cacheMoviesModel.fromResponseMovieToPersistence(searchMovie) for searchMovie in items]

        self.cacheMoviesRepository.insert_many(persistenceItems)

        repositoryIdsToSupplierIds = {}
        for persistenceItem in persistenceItems:
            repositoryIdsToSupplierIds[persistenceItem.external_id] = persistenceItem.id

        returnResult = []
        for responseMovie in items:
            cloneMovie = copy.deepcopy(responseMovie)
            cloneMovie.id = repositoryIdsToSupplierIds[responseMovie.id]

            returnResult.append(cloneMovie)

        return returnResult
