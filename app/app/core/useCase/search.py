from typing import List

from app.core.domain.search import SaveSearchInCacheInterface
from app.core.domain.search.entity import SearchMovie, SearchFilter
from app.core.domain.search.provider import Provider


class SearchUseCase():
    def __init__(
        self,
        provider: Provider,
        saveSearchInCache: SaveSearchInCacheInterface
    ) -> None:
        self.provider = provider
        self.saveSearchInCache = saveSearchInCache

    def get(self, filter: SearchFilter) -> List[SearchMovie]:
        responseItems = self.provider.get(filter=filter) # TODO

        resultItems = self.saveSearchInCache.run(responseItems)

        return resultItems
