from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.persistence.entity import CacheMovie


class Database:
    def __init__(self, database_string: str) -> None:
        print('Database created')
        self.engine = create_engine(database_string)
        self.session = sessionmaker(self.engine, expire_on_commit=False)


class AbstractRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def _insert_entity(self, entity) -> None:
        with self.database.session() as session:
            session.add(entity)
            session.commit()

    def _insert_entities(self, entities: list) -> None:
        with self.database.session() as session:
            for entity in entities:
                session.add(entity)
            session.commit()


class CacheMoviesRepository(AbstractRepository):
    def insert_many(self, entities: List[CacheMovie]) -> None:
        self._insert_entities(entities)

