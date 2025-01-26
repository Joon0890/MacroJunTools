import subprocess
import os, sys
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth

class ChromeDriverManager:
    def __init__(self):
        self._browser = None
        self._chrome_process = None

    @property
    def browser(self):
        if not self._browser:
            raise RuntimeError("[ERROR] Browser is not initialized.")
        return self._browser

    @browser.setter
    def browser(self, value):
        self._browser = value
    
    @classmethod
    def initialize_browser_with_stealth(cls, headless_flag):
        """팩토리 메서드: 인스턴스를 생성하고 로그인을 실행"""
        instance = cls()
        instance.__start_chrome_process(headless_flag)
        instance._browser = instance.__initialize_webdriver()
        __apply_stealth(instance._browser)
        return instance
    
    def __start_chrome_process(self, headless_flag):
        try:
            print("[INFO] Starting chrome process...")

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
                "--remote-debugging-port=9222",  # 디버깅 포트 설정
                "--headless" if headless_flag else "",  # 헤드리스 모드 (필요 시)
                "--disable-gpu",  # GPU 비활성화
                "--disable-dev-shm-usage",  # 공유 메모리 문제 해결
                "--no-first-run",  # 첫 실행 설정 비활성화
                "--log-level=3"
            ]
            
            # 빈 문자열 제거
            chrome_command = [arg for arg in chrome_command if arg]
            
            print(f"[INFO] Starting Chrome subprocess with command: {chrome_command}")
            
            # Chrome 서브프로세스 실행
            self._chrome_process = subprocess.Popen(chrome_command)

        except StopIteration:
            raise FileNotFoundError("[ERROR] Chrome executable not found in specified paths.")
        
        except Exception as e:
            print(f"[ERROR] Failed to start Chrome subprocess: {e}")
            raise RuntimeError("[ERROR] Chrome process failed to start")

    def __initialize_webdriver(self) -> webdriver.Chrome:
        print("[INFO] Initializing WebDriver...")
        chromedriver_autoinstaller.install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled") 

        try: 
            browser = webdriver.Chrome(options=chrome_options)
            print(f"[INFO] Created browser instance with options: {chrome_options.arguments}")
            return browser
        
        except Exception as e:
            print(f"[ERROR] Unexpected error during WebDriver initialization: {e}")
            self.terminate_process()
            raise RuntimeError("WebDriver initialization failed.")
        
    def terminate_process(self):
        # 브라우저 종료
        if self._browser:
            try:
                self._browser.quit()
                print("[INFO] WebDriver quit successfully.")
            except Exception as e:
                print(f"[WARNING] Failed to quit WebDriver: {e}")
            finally:
                self._browser = None  # 중복 종료 방지

        # Chrome 프로세스 종료
        if self._chrome_process:
            try:
                self._chrome_process.terminate()
                print("[INFO] Chrome process terminated successfully.")
            except Exception as e:
                print(f"[WARNING] Failed to terminate Chrome process: {e}")
            finally:
                self._chrome_process = None  # 중복 종료 방지

    def get_url(self, url: str, maximize_flag: bool = False, wait: int = 3):
        if maximize_flag:
            print("[INFO] maximizing chrome window...")
            self._browser.maximize_window()
        
        print(f"[INFO] Navigating to URL: {url}")
        self._browser.get(url)  
        self._browser.implicitly_wait(wait)
    
def __apply_stealth(browser):
    try:
        stealth(browser,
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