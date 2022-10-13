from typing import List, Optional

from app.core.domain.search.enum import LANGUAGES


class SearchFilter():
    def __init__(
        self,
        title: str=None,
        year: int=None
    ) -> None:
        self.title = title
        self.year = year


class MovieTitle():
    def __init__(
        self,
        language: str,
        value: str
    ) -> None:
        if language not in LANGUAGES:
            raise Exception('Language is wrong')

        self.language = language
        self.value = value


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
