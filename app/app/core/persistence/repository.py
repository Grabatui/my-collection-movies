from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests

from app.core.domain.entity import Logger
from app.core.persistence.entity import SearchHistory, CacheMovie, ExternalResponse, ExternalResponseStatusEnum


class Database():
    def __init__(self, database_string: str) -> None:
        self.engine = create_engine(database_string)
        self.session = sessionmaker(self.engine, expire_on_commit=False)


class AbstractDatabaseRepository():
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


class AbstractExternalRepository():
    def __init__(
        self,
        endpointPrefix: str
    ) -> None:
        self.__endpointPrefix = endpointPrefix

    def _post(
        self,
        endpoint: str,
        data: dict = {},
        headers: Optional[dict] = None,
        logger: Optional[Logger] = None
    ) -> ExternalResponse:
        return self.__call('POST', endpoint, data, headers, logger)

    def __call(
        self,
        method: str,
        endpoint: str,
        data: dict,
        headers: dict,
        logger: Optional[Logger]
    ) -> ExternalResponse:
        if logger:
            logger.addInfo(message='Request', data={'method': method, 'endpoint': endpoint, 'data': data, 'headers': headers})

        method = method.upper()

        request = requests.Request(
            method=method,
            url=self.__makeEndpoint(endpoint),
            json=data if method != 'GET' else None,
            params=data if method == 'GET' else None,
            headers=headers
        )

        session = requests.Session()

        try:
            response = session.send(request.prepare(), verify=False)
        except Exception as exception:
            if logger:
                logger.addError(message='EXCEPTION', data={'error': str(exception)})

            raise exception

        if logger:
            logger.addInfo(message='Response', data={'status': response.status_code, 'data': response.content})

        responseData = response.json()

        return ExternalResponse(responseData, response.status_code)

    def _makeHeaders(
        self,
        authorizationToken: Optional[str] = None
    ) -> dict:
        headers = {'Content-Type': 'application/json'}
        
        if authorizationToken is not None:
            headers['Authorization'] = 'Bearer ' + authorizationToken

        return headers

    def __makeEndpoint(self, endpoint: str) -> str:
        return self.__endpointPrefix + endpoint


class SearchHistoryRepository(AbstractDatabaseRepository):
    def insert(self, entity: SearchHistory) -> None:
        self._insert_entity(entity)


class CacheMoviesRepository(AbstractDatabaseRepository):
    def insert_many(self, entities: List[CacheMovie]) -> None:
        self._insert_entities(entities)


class AuthExternalRepository(AbstractExternalRepository):
    def checkACcessToken(self, accessToken: str, logger: Logger) -> bool:
        response = self._post(
            '/v1/check',
            headers=self._makeHeaders(accessToken),
            logger=logger
        )

        return response.getStatus() == ExternalResponseStatusEnum.success
