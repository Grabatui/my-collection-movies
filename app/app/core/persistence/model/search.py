import datetime
import json

from app.core.persistence.entity import SearchHistory, CacheMovie, SupplierEnum
from app.core.domain.search.entity import ResponseMovie, SearchMovie


class SearchHistoryModel():
    def fromQueryToPersistence(
        self,
        query: dict
    ) -> SearchHistory:
        return SearchHistory(
            query=json.dumps(query),
            inserted_at=datetime.datetime.utcnow()
        )


class SearchMovieModel():
    def fromResponseMovieToPersistence(
        self,
        searchHistoryId: int,
        domainEntity: ResponseMovie
    ) -> CacheMovie:
        return CacheMovie(
            supplier=SupplierEnum[domainEntity.supplier.value],
            external_id=domainEntity.id,
            data=json.dumps(
                domainEntity.toDictionary()
            ),
            inserted_at=datetime.datetime.utcnow(),
            search_history_id=searchHistoryId
        )

    def fromResponseMovieToSearchMovie(self, domainEntity: ResponseMovie, id: int) -> SearchMovie:
        return SearchMovie(
            id=id,
            titles=domainEntity.titles,
            year=domainEntity.year,
            rating=domainEntity.rating
        )
