from typing import List

from .entity import SearchFilter, ResponseMovie, SearchMovie


class SaveSearchHistoryInterface():
    def run(self, filter: SearchFilter) -> int:
        raise Exception('Method has to be implemented')


class SaveSearchInCacheInterface():
    def run(self, searchHistoryId: int, items: List[ResponseMovie]) -> List[SearchMovie]:
        raise Exception('Method has to be implemented')
