from app.core.domain.common import IsAccessTokenValidInterface
from app.core.domain.entity import Logger
from app.core.persistence.repository import AuthExternalRepository


class IsAccessTokenValidAction(IsAccessTokenValidInterface):
    def __init__(self, repository: AuthExternalRepository) -> None:
        self.repository = repository

    def run(self, accessToken: str, logger: Logger) -> bool:
        return self.repository.checkACcessToken(accessToken, logger)
