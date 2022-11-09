from typing import List

from app.core.domain.search import SaveSearchHistoryInterface, SaveSearchInCacheInterface
from app.core.domain.search.entity import SearchMovie, SearchFilter
from app.core.domain.search.provider import Provider


class SearchUseCase():
    def __init__(
        self,
        provider: Provider,
        saveSearchHistory: SaveSearchHistoryInterface,
        saveSearchInCache: SaveSearchInCacheInterface
    ) -> None:
        self.provider = provider
        self.saveSearchHistory = saveSearchHistory
        self.saveSearchInCache = saveSearchInCache

    def get(self, filter: SearchFilter) -> List[SearchMovie]:
        searchHistoryId = self.saveSearchHistory.run(filter)

        responseItems = self.provider.get(filter=filter)

        resultItems = self.saveSearchInCache.run(searchHistoryId, responseItems)

        return resultItems
