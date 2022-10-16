from typing import List

from app.core.domain.search.entity import ResponseMovie, SearchFilter


class SupplierInterface():
    def get(self, filter: SearchFilter) -> List[ResponseMovie]:
        raise Exception('Method has to be ovewerighted')
