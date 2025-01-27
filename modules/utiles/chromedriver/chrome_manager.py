import os
from subprocess import Popen
import chromedriver_autoinstaller
from selenium_stealth import stealth
from selenium.webdriver import Chrome, ChromeOptions

chromeDrier_running = False  # 실행 여부 확인용 플래그
DebugMode_started = False  # 프로세스 시작 여부

# Chrome 실행 경로 목록
CHROME_PATHS = [
    r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
]

# 기본 Chrome 실행 옵션
DEFAULT_OPTIONS = [
    "--remote-debugging-port=9222",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--no-first-run",
    "--log-level=3"
]

def apply_stealth(browser: Chrome):
    try:
        stealth(
            browser,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True
        )
        print("[INFO] Stealth settings applied.")
    except Exception as e:
        raise RuntimeError(f"[ERROR] Failed to apply stealth settings: {e}")
    
class ChromeSubprocessManager(Popen):
    def start_process(self, headless_flag: bool):
        """
        Starts the Chrome subprocess with the specified options.
        """
        if DebugMode_started:
            print("[WARNING] Chrome subprocess is already running.")
            return

        print("[INFO] Starting Chrome subprocess...")

        # 실행 가능한 경로 찾기
        try:
            chrome_path = next(path for path in CHROME_PATHS if os.path.exists(path))
        except StopIteration:
            raise FileNotFoundError("[ERROR] Chrome executable not found in specified paths.")

        chrome_command = [chrome_path] + DEFAULT_OPTIONS
        if headless_flag:
            chrome_command.append("--headless")

        chrome_command = [arg for arg in chrome_command if arg]  # 빈 문자열 제거

        # Popen 초기화
        try:
            super().__init__(chrome_command)  # Popen의 초기화 호출
            DebugMode_started = True
            print("[INFO] Chrome subprocess started successfully.")
        except Exception as e:
            raise RuntimeError(f"[ERROR] Failed to start Chrome subprocess: {e}")

    def terminate_process(self):
        """
        Terminates the Chrome subprocess if running.
        """
        if not DebugMode_started:
            print("[WARNING] No Chrome subprocess is running.")
            return

        try:
            self.terminate()  # Popen의 terminate 메서드 호출
            self.wait()  # 프로세스 종료 대기
            print("[INFO] Chrome subprocess terminated successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to terminate Chrome subprocess: {e}")
        finally:
            DebugMode_started = False

class OptionsManager(ChromeOptions):
    @classmethod
    def initialize_options(cls):
        """
        Initialize ChromeOptions with predefined settings.
        """
        # ChromeDriver 설치 확인
        chromedriver_autoinstaller.install()

        # ChromeOptions 객체 생성
        options = cls()  # cls()는 ChromeOptions의 서브클래스 인스턴스를 생성

        # 옵션 설정
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        options.add_argument("--disable-blink-features=AutomationControlled")

        return options

class WebDriverManager(Chrome):
    def __init__(self, chrome_options: ChromeOptions):
        """
        Initialize the Chrome WebDriver with the given options.
        """
        # 부모 클래스의 초기화를 호출하여 WebDriver 설정
        super().__init__(options=chrome_options)
        print("[INFO] WebDriver initialized successfully.")

    def navigate_to_url(self, url: str, is_maximizing: bool=True, wait: int=3):
        """
        Navigates the WebDriver to the specified URL.
        """
        try:
            print(f"[INFO] Navigating to {url}...")
            self.get(url)  # self를 WebDriver로 활용
            if is_maximizing:
                self.maximize_window()
            self.implicitly_wait(wait)
        except Exception as e:
            print(f"[ERROR] Failed to navigate to {url}: {e}")
            raise RuntimeError(f"Navigation to {url} failed.")

    def terminate_browser(self):
        """
        Terminates the WebDriver if running.
        """
        try:
            self.quit()  # Chrome(WebDriver)의 quit() 호출
            print("[INFO] WebDriver terminated successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to terminate WebDriver: {e}")

class ChromeDriverManager:
    def __init__(self):
        # 조합된 객체 초기화
        self.subprocess_manager = ChromeSubprocessManager()
        self.webdriver_manager = None  # WebDriverManager는 start 시점에 초기화
        self.options_manager = OptionsManager()

    @property
    def browser(self):
        if not self.webdriver_manager:
            raise RuntimeError("[ERROR] Browser is not initialized.")
        return self.webdriver_manager

    @browser.setter
    def browser(self, value):
        self.webdriver_manager = value

    def start(self, headless_flag: bool, url, is_maximizing: bool=True, wait: int=3):
        """
        Starts the Chrome subprocess and initializes the WebDriver.
        """
        if chromeDrier_running:
            print("[WARNING] ChromeDriverManager is already running.")
            return
        
        # 1. Chrome 서브프로세스 시작
        self.subprocess_manager.start_process(headless_flag=headless_flag)

        # 2. ChromeOptions 초기화
        chrome_options = self.options_manager.initialize_options()

        # 3. WebDriver 초기화
        self.webdriver_manager = WebDriverManager(chrome_options=chrome_options)
        self.webdriver_manager.navigate_to_url(url, is_maximizing, wait)

        # 4. Stealth 설정 적용
        apply_stealth(self.webdriver_manager)

    def stop(self):
        """
        Stops the WebDriver and the Chrome subprocess.
        """
        if chromeDrier_running:
            print("[WARNING] ChromeDriverManager is already running.")
            return
        
        if self.webdriver_manager:
            self.webdriver_manager.terminate_browser()
        self.subprocess_manager.terminate_process()

        chromeDrier_running = False
        print("[INFO] ChromeDriverManager stopped successfully.")

    
