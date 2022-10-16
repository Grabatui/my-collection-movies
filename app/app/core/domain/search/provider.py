from typing import List

from .supplier import SupplierInterface
from .supplier.kinopoisk import KinopoiskSupplier
from .entity import SearchFilter, ResponseMovie


class Provider():
    def __init__(self, kinopoisk_token: str) -> None:
        self.kinopoisk_token = kinopoisk_token

    def get(self, filter: SearchFilter) -> List[ResponseMovie]:
        result = []
        for supplier in self.__get_suppliers():
            result.extend(supplier.get(filter))

        return result

    def __get_suppliers(self) -> List[SupplierInterface]:
        return (
            KinopoiskSupplier(self.kinopoisk_token),
        )
