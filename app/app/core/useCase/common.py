from app.core.domain.common import IsAccessTokenValidInterface
from app.core.domain.entity import Logger


class ValidateAccessTokenUseCase():
    def __init__(
        self,
        isAccessTokenValid: IsAccessTokenValidInterface,
        logRootPath: str
    ) -> None:
        self.isAccessTokenValid = isAccessTokenValid
        self.logRootPath = logRootPath

    def run(self, accessToken: str) -> None:
        logger = Logger(self.__class__.__name__, self.logRootPath)

        if not self.isAccessTokenValid.run(accessToken, logger):
            raise Exception('Access token is invalid')
