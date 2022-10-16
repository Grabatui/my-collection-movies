from typing import List

from .entity import ResponseMovie, SearchMovie


class SaveSearchInCacheInterface():
    def run(self, items: List[ResponseMovie]) -> List[SearchMovie]:
        raise Exception('Method has to be ovewerighted')
