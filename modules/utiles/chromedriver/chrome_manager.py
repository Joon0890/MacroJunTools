import os
import sys
import socket
import pickle
import logging
from subprocess import Popen, PIPE
import chromedriver_autoinstaller
from selenium_stealth import stealth
from selenium.webdriver import Chrome, ChromeOptions
from modules.utiles.logging.logging_utils import GetLogger

logger = GetLogger()

# Chrome 실행 경로 목록
CHROME_PATHS = [
    r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
]

DEFAULT_OPTIONS = [
    "--disable-gpu",
    "--window-size=1920,1080",
    "--disable-dev-shm-usage",
    "--no-first-run",
]               

def find_available_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # OS가 사용 가능한 포트를 자동 할당
        return s.getsockname()[1]
    
class ChromeSubprocessManager:
    def __init__(self):
        self.process = None

    def start_process(self, available_port, args, headless: bool):
        logger.info("Starting Chrome subprocess...")
        
        try:
            chrome_path = next(path for path in CHROME_PATHS if os.path.exists(path))
        except StopIteration:
            logger.error("Chrome executable not found.")
            raise FileNotFoundError("Chrome executable not found.")

        chrome_command = [chrome_path] + args
        chrome_command.append(f"--remote-debugging-port={available_port}")
        if headless:
            chrome_command.append("--headless=new") 
        try:
            self.process = Popen(chrome_command, stdout=PIPE, stderr=PIPE)
            logger.info("Chrome subprocess started.")
        except Exception as e:
            logger.error("Failed to start Chrome subprocess: %s", e)
            raise

    def terminate_process(self):
        if not self.process:
            return False
        try:
            self.process.terminate()
            logger.info("Chrome subprocess terminated.")
            self.process = None  # 프로세스 정리
            return True
        except Exception as e:
            logger.error("Failed to terminate Chrome subprocess: %s", e)
            return False


class WebDriverManager:
    def __init__(self):
        self.browser = None

    def start_driver(self, available_port):
        chromedriver_autoinstaller.install()
        options = ChromeOptions()
        options.add_experimental_option("debuggerAddress", f"127.0.0.1:{available_port}")
        options.add_argument("--disable-blink-features=AutomationControlled")

        try:
            self.browser = Chrome(options=options)
            logger.info("WebDriver initialized.")
        except Exception as e:
            logger.error("Failed to start WebDriver: %s", e)
            raise

    def navigate_to(self, url: str, maximize: bool = True, wait: int = 3):
        if not self.browser:
            logger.error("WebDriver is not initialized.")
            return

        try:
            logger.info("Navigating to %s...", url)
            self.browser.get(url)

            if maximize:
                self.browser.maximize_window()
            self.browser.implicitly_wait(wait)
        except Exception as e:
            logger.error("Failed to navigate to %s: %s", url, e)

    def apply_stealth(self):
        if not self.browser:
            return
        try:
            stealth(
                self.browser,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True
            )
            
            logger.info("Stealth settings applied.")
        except Exception as e:
            logger.warning("Failed to apply stealth settings: %s", e)

    def quit_driver(self):
        if self.browser:
            self.browser.quit()
            logger.info("WebDriver terminated.")
            self.browser = None  # WebDriver 정리

class ChromeDriverManager:
    def __init__(self):
        self.subprocess_manager = ChromeSubprocessManager()
        self.webdriver_manager = WebDriverManager()
        self.is_running = False

    @property
    def browser(self) -> "Chrome":
        if not self.webdriver_manager.browser:
            logging.error("Browser is not initialized")
        return self.webdriver_manager.browser

    @browser.setter
    def browser(self, value):
        self.webdriver_manager.browser = value

    def start(self, available_port, headless: bool, url, maximize: bool = True, wait: int = 3):
        if self.is_running:
            logger.warning("ChromeDriverManager is already running.")
            return

        try:
            available_port = find_available_port()
            self.subprocess_manager.start_process(available_port, DEFAULT_OPTIONS, headless)
            self.webdriver_manager.start_driver(available_port)
            self.webdriver_manager.navigate_to(url, maximize, wait)
            self.webdriver_manager.apply_stealth()
            self.is_running = True
        except Exception as e:
            logger.error("Failed to start ChromeDriverManager: %s", e)
            self.stop()  # 예외 발생 시 안전하게 정리
            raise

    def stop(self):
        """ Chrome 및 WebDriver 안전 종료 """
        if self.subprocess_manager.process:
            self.subprocess_manager.terminate_process()

        self.is_running = False
        logger.info("ChromeDriverManager stopped.")


if __name__ == "__main__":
    try:
        manager = ChromeDriverManager()
        manager.start(headless=False, url="https://everytime.kr/")

        input("Press Enter to stop...")  # 테스트용

    except KeyboardInterrupt:
        logger.info("User interrupted execution. Stopping ChromeDriverManager.")
    except Exception as e:
        logger.error("Unexpected error: %s", e)
    finally:
        manager.stop()
        sys.exit(0)  # 프로그램 정상 종료
