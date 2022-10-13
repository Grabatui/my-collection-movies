from typing import List

from app.core.domain.search.entity import SearchMovie, SearchFilter
from app.core.domain.search.provider import Provider


class SearchUseCase():
    def __init__(self, provider: Provider) -> None:
        self.provider = provider

    def get(self, filter: SearchFilter) -> List[SearchMovie]:
        return self.provider.get(filter=filter)
