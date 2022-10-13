from typing import List

from app.core.domain.search.entity import SearchMovie, SearchFilter


class SupplierInterface():
    def get(self, filter: SearchFilter) -> List[SearchMovie]:
        raise Exception('Method has to be ovewerighted')
