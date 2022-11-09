import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pythonjsonlogger import jsonlogger


class Logger():
    def __init__(self, name: str, rootPath: str) -> None:
        self.__name = name
        self.__rootPath = rootPath
        self.__logger = self.__makeLogger()

    def addInfo(self, message: str = '', data: dict = {}):
        self.__logger.info(message, extra=data)

    def addError(self, message: str = '', data: dict = {}):
        self.__logger.error(message, extra=data)

    def __makeLogger(self) -> logging.Logger:
        logger = logging.getLogger(self.__name)
        logger.level = logging.DEBUG

        logFullPath = os.path.join(self.__rootPath, 'logs', 'log.log')
        logHandler = TimedRotatingFileHandler(logFullPath, when='midnight')
        
        logFormatter = jsonlogger.JsonFormatter()
        
        logHandler.setFormatter(logFormatter)
        
        logger.addHandler(logHandler)

        return logger