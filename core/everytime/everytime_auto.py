import os
from selenium.common.exceptions import NoSuchElementException
from core.everytime.articles import move_to_board, find_starting_point
from core.everytime.autolike import EverytimeAutoLiker
from core.everytime.login import login_everytime
from core.utils.custom_logging import GetLogger
from core.utils.file.env_utils import load_env
from core.utils.chrome_manager import ChromeDriverService
from core.everytime.transform import _selenium_error_transform

class RunEverytimeAutoLike(ChromeDriverService):
    def __init__(self, logging_file_path="./logs/everytime_autolike.log"):
        super().__init__()
        self.logging_file_path = logging_file_path
        os.makedirs('./logs', exist_ok=True)
        self.logger = GetLogger("logger_everytime", logging_file_path)
        self.start_running()
        
    def get_id_password(self):
        my_id = os.environ.get('EVERYTIME_USERNAME')
        my_password = os.environ.get('EVERYTIME_PASSWORD')
        print("Everytime ID, Password: %s, %s", my_id, my_password)
        
        if not my_id or not my_password:
            print("Everytime ID, Password are missing in .env file!")
            raise

        return my_id, my_password
    
    def start_running(self):
        print("Starting Everytime auto-like...")
        
        try:
            self.start(url="https://everytime.kr/")

            # 크롬이 종료되었을 경우 예외 처리
            if not self.browser:
                print("Chrome browser failed to start.")
                raise SystemExit("Chrome browser failed to start.")

            login_everytime(self.browser, self.logger, *self.get_id_password())
            move_to_board(self.browser, self.logger, "자유게시판")
            start_article, page_num = find_starting_point(self.browser, self.logger, self.logging_file_path)

            print("Starting from article: %s, page number: %s", start_article, page_num)

            EverytimeAutoLiker.start(self.browser, self.logger, start_article, page_num)

        except NoSuchElementException:
            print("Exiting program as there are no more elements to process.")
            raise 

        except Exception as e:
            print(f"An unknown error occurred: {str(e).strip()}")
            raise

        finally:
            self.stop()
            print("The task is complete.")
            return 