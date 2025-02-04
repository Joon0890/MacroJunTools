import sys
from functools import wraps
from modules.utiles.logging.logging_utils import GetLogger
from selenium.common.exceptions import NoSuchElementException, WebDriverException, NoSuchWindowException
from modules.everytime.scripts.transform import selenium_error_transform
logger = GetLogger()

def exception_handler(logger):
    """
    - `KeyboardInterrupt`: 프로그램 종료
    - `WebDriverException`, `NoSuchWindowException`: 크롬 드라이버 문제로 종료
    - 일반 `Exception`: 예상치 못한 오류로 종료
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            
            except KeyboardInterrupt:
                logger.info("Program interrupted by the user. Exiting gracefully.")
                manager = args[0] if hasattr(args[0], "stop") else None
                if manager:
                    manager.stop()
                sys.exit("Execution stopped by user (Ctrl+C).")
            
            except NoSuchElementException as e:
                # The login method should continue even if an element is not found
                logger.warning(f"Element not found, proceeding to the next step: {selenium_error_transform(e)}")
                raise e
            
            except (WebDriverException, NoSuchWindowException) as e:
                logger.error(f"ChromeDriver connection lost: {selenium_error_transform(e)}")
                manager = args[0] if hasattr(args[0], "stop") else None
                if manager:
                    manager.stop()
                sys.exit("Terminating due to ChromeDriver connection failure.")

            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                manager = args[0] if hasattr(args[0], "stop") else None
                if manager:
                    manager.stop()
                sys.exit("Terminating due to an unknown error.")

        return wrapper
    return decorator