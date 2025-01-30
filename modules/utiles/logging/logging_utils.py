import os
import logging
from modules.utiles.logging.logger import CustomLogging

class GetLogger:
    _instance = None  # 하나의 전역 로거 유지

    def __new__(cls, logger_name="everytime_autoLike.log", logger_option="GlobalLogger"):
        if cls._instance is None:
            logger = CustomLogging(logger_option)  # 하나의 글로벌 로거 생성

            if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
                logger.addHandler(logger_name)

            cls._instance = logger  # 인스턴스 저장

        return cls._instance  # 동일한 로거 반환
