from __future__ import annotations
from typing import List, Optional
from enum import Enum


class SearchFilter():
    def __init__(
        self,
        title: str=None,
        year: int=None
    ) -> None:
        self.title = title
        self.year = year


class LanguageEnum(Enum):
    ru = 'ru'
    en = 'en'


class MovieTitle():
    def __init__(
        self,
        language: LanguageEnum,
        value: str
    ) -> None:
        self.language = language
        self.value = value

    def toDictionary(self) -> dict:
        return {
            'language': self.language.name,
            'value': self.value
        }

    def fromDictionary(dictionary: dict) -> MovieTitle:
        return MovieTitle(
            language=LanguageEnum[dictionary['language']],
            value=dictionary['value']
        )


class SupplierEnum(Enum):
    kinopoisk = 'kinopoisk'


class ResponseMovie():
    def __init__(
        self,
        id: int,
        supplier: SupplierEnum,
        titles: List[MovieTitle],
        year: Optional[int],
        rating: float
    ) -> None:
        self.id = id
        self.supplier = supplier
        self.titles = titles
        self.year = year
        self.rating = rating

    def toDictionary(self) -> dict:
        return {
            'id': self.id,
            'supplier': self.supplier.name,
            'titles': [movieTitle.toDictionary() for movieTitle in self.titles],
            'year': self.year,
            'rating': self.rating
        }

    def fromDictionary(dictionary: dict) -> ResponseMovie:
        return ResponseMovie(
            id=dictionary['id'],
            supplier=SupplierEnum[dictionary['supplier']],
            titles=[MovieTitle.fromDictionary(movieTitle) for movieTitle in dictionary['titles']],
            year=dictionary['year'],
            rating=dictionary['rating']
        )


class SearchMovie():
    def __init__(
        self,
        id: int,
        titles: List[MovieTitle],
        year: Optional[int],
        rating: float
    ) -> None:
        self.id = id
        self.titles = titles
        self.year = year
        self.rating = rating
