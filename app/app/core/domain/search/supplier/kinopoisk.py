from typing import List
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest
from kinopoisk_unofficial.model.dictonary.found_film import FoundFilm

from app.core.domain.search.entity import SearchMovie, MovieTitle, SearchFilter
from app.core.domain.search import enum
from . import SupplierInterface


class KinopoiskSupplier(SupplierInterface):
    def __init__(self, token: str) -> None:
        self.token = token

    def get(self, filter: SearchFilter) -> List[SearchMovie]:
        query = self.__make_query(filter)

        if not query:
            return []

        raw_items = self.__search_movies_by_query(query)

        return list(map(self.__process_movie, raw_items))

    def __make_query(self, filter: SearchFilter) -> str:
        query = []
        if filter.title:
            query.append(filter.title)

        if filter.year:
            query.append(str(filter.year))

        return ', '.join(query)

    def __search_movies_by_query(self, query: str) -> List[FoundFilm]:
        api_client = KinopoiskApiClient(self.token)
        
        response = api_client.films.send_search_by_keyword_request(
            SearchByKeywordRequest(query)
        )

        return response.films

    def __process_movie(self, raw_movie: FoundFilm) -> SearchMovie:
        return SearchMovie(
            id=raw_movie.film_id,
            titles=[
                MovieTitle(enum.LANGUAGE_EN, raw_movie.name_en),
                MovieTitle(enum.LANGUAGE_RU, raw_movie.name_ru)
            ],
            year=int(raw_movie.year) if raw_movie.year is not None else None,
            rating=float(raw_movie.rating) if raw_movie.rating is not None and raw_movie.rating != 'null' else 0.0
        )
