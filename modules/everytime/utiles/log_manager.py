import logging
import csv

# CSV 핸들러 정의
class CSVLoggingHandler(logging.Handler):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.file = open(filename, mode='a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        # CSV 헤더 추가 (처음에만 추가)
        self.writer.writerow(["Timestamp", "Level", "Message"])

    def emit(self, record):
        log_entry = self.format(record)
        timestamp = self.formatTime(record)
        level = record.levelname
        message = record.msg
        self.writer.writerow([timestamp, level, message])

    def close(self):
        self.file.close()
        super().close()

# 로거 설정
logger = logging.getLogger("DualLogger")
logger.setLevel(logging.DEBUG)

# 텍스트 로그 파일 핸들러
text_file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
text_file_handler.setLevel(logging.DEBUG)
text_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# CSV 로그 파일 핸들러
csv_file_handler = CSVLoggingHandler("app.csv")
csv_file_handler.setLevel(logging.DEBUG)

# 로거에 핸들러 추가
logger.addHandler(text_file_handler)
logger.addHandler(csv_file_handler)

# 로깅 테스트
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
