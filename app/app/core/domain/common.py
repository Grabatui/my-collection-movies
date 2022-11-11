from app.core.domain.entity import Logger


class IsAccessTokenValidInterface():
    def run(self, accessToken: str, logger: Logger) -> bool:
        pass


class LoggerProvider():
    def __init__(self, logRootPath: str) -> None:
        self.logRootPath = logRootPath

    def get(self, name: str) -> Logger:
        return Logger(name, self.logRootPath)
