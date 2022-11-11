from app.core.domain.common import IsAccessTokenValidInterface, LoggerProvider


class ValidateAccessTokenUseCase():
    def __init__(
        self,
        isAccessTokenValid: IsAccessTokenValidInterface,
        loggerProvider: LoggerProvider
    ) -> None:
        self.isAccessTokenValid = isAccessTokenValid
        self.loggerProvider = loggerProvider

    def run(self, accessToken: str) -> None:
        logger = self.loggerProvider.get(self.__class__.__name__)

        if not self.isAccessTokenValid.run(accessToken, logger):
            raise Exception('Access token is invalid')
