import os
import csv
import logging
from datetime import datetime

class CustomFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%', validate=True):
        if not fmt:
            fmt = "%(asctime)s - %(levelname)s - %(relpath)s:%(lineno)d - %(funcName)s - %(message)s"
        super().__init__(fmt, datefmt, style, validate)  # 부모 클래스의 __init__ 호출

    def format(self, record):
        # record.pathname은 전체 경로
        record.relpath = os.path.relpath(record.pathname)  # 상대경로 추가
        return super().format(record)
    
    def formatTime(self, record, datefmt=None):
        # 원하는 형식을 명시
        datefmt = datefmt or '%Y-%m-%d %H:%M:%S'  # Default: YYYY-MM-DD HH:MM:SS,ms
        ct = self.converter(record.created)  # 기본 시간 변환기 사용 (localtime)
        return datetime.fromtimestamp(record.created).strftime(datefmt)

class BaseFileHandler(logging.Handler):
    def __init__(self, filename, mode='a', encoding='utf-8', level=logging.DEBUG):
        super().__init__(level)
        self.filename = filename
        self.file = open(filename, mode=mode, encoding=encoding, newline='')

    def close(self):
        if not self.file.closed:
            self.file.close()
        super().close()

class FileLoggingHandler(BaseFileHandler):
    def __init__(self, filename, mode='a', encoding=None, level=logging.DEBUG):
        super().__init__(filename, mode, encoding, level)

    def emit(self, record):
        try:
            formatted_message = self.formatter.format(record)  # 포맷된 메시지
            self.file.write(formatted_message + "\n")
            self.file.flush()  # 파일에 즉시 기록
        except Exception:
            self.handleError(record)

class CustomLogging(logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        self.setLevel(logging.DEBUG)

    def add_handler(self, filename, fmt=None, mode='a', level=logging.DEBUG, encoding='utf-8'):
        handler = FileLoggingHandler(filename, mode, level, encoding)
        handler.setFormatter(CustomFormatter(fmt))
        super().addHandler(handler)
    
if __name__=="__main__":
    # 로거 설정
    logger = CustomLogging("DualLogger")
    logger.add_handler("app.log")

    # 로깅 테스트
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
