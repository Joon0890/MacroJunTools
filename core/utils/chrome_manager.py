import tempfile, os, shutil
from typing import Optional
from subprocess import Popen
from selenium_stealth import stealth
import os, socket, shlex, platform, traceback
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import SessionNotCreatedException

# SYSTEM = platform.system()
SYSTEM = 'Linux'

def find_available_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # OS가 사용 가능한 포트를 자동 할당
        return s.getsockname()[1]

def find_chrome_path(CHROME_PATHS) -> Optional[str]:
    """CHROME_PATHS 중 존재하는 실행 파일 경로를 반환"""
    return next((path for path in CHROME_PATHS if os.path.exists(path)), None)

def get_user_agent():
    if SYSTEM == "Windows":
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    elif SYSTEM == "Linux":
        return "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    elif SYSTEM == "Darwin":  # MacOS
        return "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"

def _get_chrome_paths() -> list[str]:
    if SYSTEM == "Windows":
        return [
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        ]
    elif SYSTEM == "Linux":
        # GitHub Actions (Ubuntu)의 기본 Chrome 경로 추가
        return [r"/usr/bin/google-chrome"]
    elif SYSTEM == "Darwin": # MacOS
        return [r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    return []

class ChromeProcessManager:
    CHROME_OPTIONS = [
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--no-first-run",
        "--log-level=3"
    ]

    def __init__(self):
        self.process: Optional[Popen] = None

    @property
    def paths(self):
        return self.CHROME_PATHS
    
    @paths.setter
    def paths(self, value):
        self.CHROME_PATHS = value

    @property
    def options(self):
        return self.CHROME_OPTIONS
    
    @options.setter
    def options(self, value):
        self.CHROME_OPTIONS = value

    def start_chrome(self, headless: bool, available_port: int):
        self.CHROME_OPTIONS.append(f"--user-data-dir={tempfile.mkdtemp()}")
        chrome_path = find_chrome_path(_get_chrome_paths())
        chrome_command = [chrome_path] + self.CHROME_OPTIONS
        chrome_command.append(f"--remote-debugging-port={available_port}")
        if headless:
            chrome_command.append("--headless")
        self.process = Popen(chrome_command)

    def stop_chrome(self) -> bool:
        if self.process:
            self.process.terminate()
            self.process = None  

class WebDriverController:
    def __init__(self):
        self.browser: Optional["Chrome"] = None

    def _build_options(self, headless: bool):
        opts = ChromeOptions()
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_argument(f"--user-agent={get_user_agent()}")
        opts.add_argument("--lang=ko_KR")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--no-first-run")
        opts.add_argument("--no-default-browser-check")
        opts.add_argument("--remote-debugging-port=0")  # 충돌 회피
        self._tmp_profile = tempfile.mkdtemp(prefix="chrome_user_")
        opts.add_argument(f"--user-data-dir={self._tmp_profile}")
        if headless:
            opts.add_argument("--headless=new")
        print(f"[Chrome] user-data-dir: {self._tmp_profile}")
        print(f"[Chrome] args: {opts.arguments}")
        return opts

    def start_driver(self, headless: bool=False, retries: int=1):
        attempt = 0
        last_exc = None
        while attempt <= retries:
            try:
                service = Service()
                options = self._build_options(headless)
                self.browser = Chrome(service=service, options=options)
                return  # 성공
            except SessionNotCreatedException as e:
                msg = str(e)
                last_exc = e
                # 현재 프로필 정리 후 재시도
                if self._tmp_profile:
                    shutil.rmtree(self._tmp_profile, ignore_errors=True)
                    self._tmp_profile = None
                if "user data directory is already in use" in msg and attempt < retries:
                    attempt += 1
                    continue
                raise  # 다른 원인이거나 재시도 소진
            except Exception as e:
                # 다른 예외
                # 실패해도 프로필 정리
                if self._tmp_profile:
                    shutil.rmtree(self._tmp_profile, ignore_errors=True)
                    self._tmp_profile = None
                raise
        if last_exc:
            raise last_exc


    def start_driver(self, available_port: int, headless: bool=False):
        service = Service()
        options = ChromeOptions()

        if not (SYSTEM == 'Linux'):
            options.add_experimental_option("debuggerAddress", f"127.0.0.1:{available_port}")
        
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-agent={get_user_agent()}")
        options.add_argument("--lang=ko_KR")
        options.add_argument("--window-size=1920,1080")

        if SYSTEM == 'Linux':
            self._tmp_profile = tempfile.mkdtemp(prefix='chrome_user_')
            options.add_argument(f"--user-data-dir={self._tmp_profile}")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        if headless:
            options.add_argument("--headless=new") 

        print(f"[Chrome] user-data-dir: {self._tmp_profile or '(default)'}")

             
        self.browser = Chrome(service=service, options=options)

    def navigate_to(self, url, maximize, wait):  
        self.browser.get(url)
        # if maximize:
        #     self.browser.maximize_window()
        self.browser.implicitly_wait(wait)
       
    def quit_driver(self):
        if self.browser:
            self.browser.quit() 
            self.browser = None  # WebDriver 정리

        if self._tmp_profile:
            shutil.rmtree(self._tmp_profile, ignore_errors=True)
            self._tmp_profile = None


class AdvancedStealthService:
    def __init__(self, stealth_config=None):
        self.stealth_config = stealth_config or {
            "languages": ["en-US", "en"],
            "vendor": "Google Inc.",
            "platform": "Win32",
            "webgl_vendor": "Intel Inc.",
            "renderer": "Intel Iris OpenGL Engine",
            "fix_hairline": True
        }

    def apply_stealth(self, browser):
        self._apply_stealth_library(browser, self.stealth_config)
        self._apply_additional_stealth(browser)

    def _apply_stealth_library(self, browser, stealth_config):
        stealth(browser, **stealth_config)

    def _apply_additional_stealth(self, browser: Chrome):
        scripts = [
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
            "window.navigator.chrome = {runtime: {}};",
            "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",
            "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
        ]

        for script in scripts:
            browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
            
class ChromeDriverService(WebDriverController):
    def __init__(self, args=None, paths=None, stealth_config=None):
        self.process_manager: ChromeProcessManager = ChromeProcessManager()
        self.stealth_manager: AdvancedStealthService = AdvancedStealthService(stealth_config)
        super().__init__()

        if args is not None:
            if isinstance(args, str):
                self.process_manager.options = shlex.split(args)
            elif isinstance(args, list):
                self.process_manager.options = args
            else:
                raise TypeError("paths must be a list of strings")
        
        if paths is not None:
            if isinstance(paths, list):
                self.process_manager.paths = paths
            else:
                raise TypeError("paths must be a string")
            
    def __enter__(self) -> "ChromeDriverService":
        return self  # 객체 자체를 반환

    def __exit__(self, exc_type, exc_value, traceback_obj) -> bool:      
        self.stop()  # 안전한 종료 처리
        
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, traceback_obj)
        
            if exc_type is KeyboardInterrupt:
                return True  # Ctrl+C 예외 무시
            
        return False  # 예외를 다시 발생시켜 상위 코드에서 처리할 수 있도록 함.

    def start(self, url, headless: bool, maximize: bool = True, wait: int = 3):
        available_port = find_available_port()
        if not (SYSTEM == 'Linux'):
            self.process_manager.start_chrome(headless, available_port)
        self.start_driver(available_port)
        self.navigate_to(url, maximize, wait)

    def stop(self):
        if self.process_manager.process:
            self.process_manager.stop_chrome()
        if self.browser: 
            self.quit_driver()
    
if __name__=='__main__':
    chromedriver = ChromeDriverService()

    chromedriver.start("https://www.naver.com", False)
    input("브라우저를 닫지 않고 유지합니다. 종료하려면 Enter를 누르세요.\n")