import enum

from sqlalchemy import Column, Integer, String, Enum, Text, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class SupplierEnum(enum.Enum):
    kinopoisk = 'kinopoisk'

class CacheMovie(Base):
    __tablename__ = 'cache_movies'

    id = Column(Integer, primary_key=True)
    supplier = Column(Enum(SupplierEnum), nullable=False)
    external_id = Column(String, nullable=False)
    data = Column(Text, nullable=False)
    inserted_at = Column(DateTime, nullable=False)

    def __repr__(self) -> str:
         return f'CacheMovie(id={self.id!r}, supplier={self.supplier!r}, external_id={self.external_id!r})'