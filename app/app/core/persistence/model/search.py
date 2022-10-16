import datetime
import json

from app.core.persistence.entity import CacheMovie, SupplierEnum
from app.core.domain.search.entity import ResponseMovie


class CacheMovieModel():
    def fromResponseMovieToPersistence(self, domainEntity: ResponseMovie) -> CacheMovie:
        return CacheMovie(
            supplier=SupplierEnum[domainEntity.supplier.value],
            external_id=domainEntity.id,
            data=json.dumps(
                domainEntity.toDictionary()
            ),
            inserted_at=datetime.datetime.utcnow()
        )
