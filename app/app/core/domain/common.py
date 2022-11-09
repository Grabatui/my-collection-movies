from app.core.domain.entity import Logger


class IsAccessTokenValidInterface():
    def run(self, accessToken: str, logger: Logger) -> bool:
        pass
