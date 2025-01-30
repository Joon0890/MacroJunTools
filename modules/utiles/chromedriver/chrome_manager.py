import os
import sys
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
    "--remote-debugging-port=9222",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--no-first-run",
    "--log-level=3"
]

class ChromeSubprocessManager:
    def __init__(self):
        self.process = None

    def start_process(self, args, headless: bool):
        logger.info("Starting Chrome subprocess...")
        
        try:
            chrome_path = next(path for path in CHROME_PATHS if os.path.exists(path))
        except StopIteration:
            logger.error("Chrome executable not found.")
            raise FileNotFoundError("Chrome executable not found.")

        chrome_command = [chrome_path] + args
        if headless:
            chrome_command.append("--headless")

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

    def start_driver(self):
        chromedriver_autoinstaller.install()
        options = ChromeOptions()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
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

    def start(self, headless: bool, url, maximize: bool = True, wait: int = 3):
        if self.is_running:
            logger.warning("ChromeDriverManager is already running.")
            return

        try:
            self.subprocess_manager.start_process(DEFAULT_OPTIONS, headless)
            self.webdriver_manager.start_driver()
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
