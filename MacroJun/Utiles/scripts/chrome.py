import subprocess, os
from selenium import webdriver
import chromedriver_autoinstaller
from selenium_stealth import stealth

class ChromeDriverManager:
    def __init__(self, headless_flag: bool, close_flag: bool = True):
        self.close_flag = close_flag
        self.headless_flag = headless_flag
        self.browser = None
        self.__chrome_process = None
        self._start_chrome_process()
        self.browser = self._initialize_webdriver()
        self._apply_stealth()
        
    def __enter__(self):
        """Returns the WebDriver instance when entering the context."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensures that resources are cleaned up on exiting the context."""
        if self.close_flag:
            self._terminate_process()

    def _start_chrome_process(self):
        try:
            # Chrome 실행 경로 (기본 경로와 대체 경로를 리스트로 저장)
            chrome_paths = [
                r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
                r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            ]
            
            # 실행할 Chrome 경로 설정
            chrome_path = next(path for path in chrome_paths if os.path.exists(path))
            
            # Chrome 실행 명령어
            chrome_command = [
                chrome_path,
                "--remote-debugging-port=9222",
                "--headless" if self.headless_flag else "",  # 헤드리스 모드 (필요 시)
                "--disable-gpu",  # GPU 비활성화
                "--disable-dev-shm-usage",  # 공유 메모리 문제 해결
                "--no-first-run",  # 첫 실행 설정 비활성화
                "--user-data-dir=C:\\chrometemp"
            ]
            
            # 빈 문자열 제거
            chrome_command = [arg for arg in chrome_command if arg]
            
            print(f"[INFO] Starting Chrome subprocess with command: {chrome_command}")
            
            # Chrome 서브프로세스 실행
            self.__chrome_process = subprocess.Popen(
                chrome_command
            )

        except StopIteration:
            raise FileNotFoundError("[ERROR] Chrome executable not found in specified paths.")
        
        except Exception as e:
            print(f"[ERROR] Failed to start Chrome subprocess: {e}")
            raise RuntimeError("[ERROR] Chrome process failed to start")

    def _initialize_webdriver(self) -> webdriver.Chrome:
        print("[INFO] Initializing WebDriver...")
        chromedriver_autoinstaller.install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
        
        try:
            return webdriver.Chrome(options=chrome_options)
        
        except Exception as e:
            print(f"[ERROR] Failed to initialize WebDriver: {e}")
            self._terminate_process()
            raise RuntimeError("WebDriver initialization failed.")
    
    def _apply_stealth(self):
        try:
            stealth(self.browser,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True)
            print("[INFO] Stealth settings successfully applied.")
        except Exception as e:
            print(f"[ERROR] Failed to apply stealth settings: {e}")
            raise RuntimeError("Failed to apply stealth settings.")
        
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
        if maximize_flag:
            browser.maximize_window()
        print(f"[INFO] Navigating to URL: {url}")
        browser.get(url)
        browser.implicitly_wait(wait)

    def get_browser(self):
        if not self.browser:
            raise RuntimeError("[ERROR] Browser is not initialized.")
        return self.browser
    
