import subprocess, shlex
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class ChromeDriverManager:
    DEFAULT_OPTIONS = [
        "--remote-debugging-port=9221",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-extensions",
        "--disable-plugins",
        "--disable-infobars",
        "--disable-blink-features=AutomationControlled",
    ]

    def __init__(self, desktop_flags: bool = True, close_flag: bool = True, headless_flag: bool = False):
        self.desktop_flags = desktop_flags
        self.close_flag = close_flag
        self.headless_flag = headless_flag
        self.browser = None
        self.__chrome_process = None
        self._start_chrome_process()
        self.browser = self._initialize_webdriver()

    def __enter__(self):
        """Returns the WebDriver instance when entering the context."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensures that resources are cleaned up on exiting the context."""
        if self.close_flag:
            self._terminate_process()

    def _start_chrome_process(self):
        program_files = "Program Files (x86)" if self.desktop_flags else "Program Files"
        chrome_path = f"C:\\{program_files}\\Google\\Chrome\\Application\\chrome.exe"
        chrome_command = f'"{chrome_path}" --remote-debugging-port=9222 --user-data-dir=tmp'

        try:
            print(f"[INFO] Starting Chrome subprocess with command: {chrome_command}")
            self.__chrome_process = subprocess.Popen(shlex.split(chrome_command))
        except FileNotFoundError:
            raise RuntimeError("[ERROR] Chrome executable not found.")
        except Exception as e:
            print(f"[ERROR] Failed to start Chrome subprocess: {e}")
            raise RuntimeError("[ERROR] Chrome process failed to start")

    def _initialize_webdriver(self) -> webdriver.Chrome:
        print("[INFO] Initializing WebDriver...")
        chromedriver_autoinstaller.install()
        chrome_options = webdriver.ChromeOptions()

        # 디버거 연결
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        # 헤드리스 모드 적용
        if self.headless_flag:
            print("[INFO] Enabling headless mode...")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")

        try:
            return webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"[ERROR] Failed to initialize WebDriver: {e}")
            self._terminate_process()
            raise RuntimeError("WebDriver initialization failed.")

    def _terminate_process(self):
        if self.browser:
            try:
                self.browser.quit()
            except Exception as e:
                print(f"[WARNING] Failed to quit WebDriver: {e}")
        if self.__chrome_process:
            try:
                self.__chrome_process.terminate()
            except Exception as e:
                print(f"[WARNING] Failed to terminate Chrome process: {e}")

    def get_url(self, url: str, maximize_flag: bool = False, wait: int = 3):
        browser = self.get_browser()
        if maximize_flag and not self.headless_flag:
            browser.maximize_window()
        print(f"[INFO] Navigating to URL: {url}")
        browser.get(url)
        browser.implicitly_wait(wait)

    def get_browser(self):
        if not self.browser:
            raise RuntimeError("[ERROR] Browser is not initialized.")
        return self.browser


def wait_for_element(browser, by, value, timeout=10):
    """Waits for an element to appear and returns it."""
    return WebDriverWait(browser, timeout).until(EC.presence_of_element_located((by, value)))

def scroll_into_view(browser: webdriver.Chrome, element):
    """Scrolls the browser to bring the element into view."""
    SCROLL_SCRIPT = "arguments[0].scrollIntoView({ behavior: 'auto', block: 'center', inline: 'center' });"
    browser.execute_script(SCROLL_SCRIPT, element); sleep(1)