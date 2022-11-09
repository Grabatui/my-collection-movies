import enum

from sqlalchemy import Column, Integer, String, Enum, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class SupplierEnum(enum.Enum):
    kinopoisk = 'kinopoisk'


class SearchHistory(Base):
    __tablename__ = 'search_history'

    id = Column(Integer, primary_key=True)
    query = Column(String, nullable=False)
    inserted_at = Column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f'SearchHistory(id={self.id!r}, query={self.query!r})'


class CacheMovie(Base):
    __tablename__ = 'search_movies'

    id = Column(Integer, primary_key=True)
    supplier = Column(Enum(SupplierEnum), nullable=False)
    external_id = Column(String, nullable=False)
    data = Column(Text, nullable=False)
    inserted_at = Column(DateTime, nullable=False)
    search_history_id = Column(Integer, ForeignKey('search_history.id'))

    def __repr__(self) -> str:
         return f'CacheMovie(id={self.id!r}, supplier={self.supplier!r}, external_id={self.external_id!r})'


class ExternalResponseStatusEnum(enum.Enum):
    success = 'success'
    error = 'error'


class ExternalResponse():
    def __init__(self, data: dict, statusCode: str) -> None:
        self.data = data
        self.statusCode = statusCode

    def getStatus(self) -> ExternalResponseStatusEnum:
        return ExternalResponseStatusEnum(self.data['status'])
