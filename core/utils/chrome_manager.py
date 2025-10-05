import tempfile, os, shutil
import chromedriver_autoinstall
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

    # def _build_options(self, headless: bool):
    #     options = ChromeOptions()
    #     # 헤드리스 필수 옵션
    #     options.add_argument('--headless=new')
    #     options.add_argument('--no-sandbox')
    #     options.add_argument('--disable-dev-shm-usage')
        
    #     # 리눅스 헤드리스 특화 옵션
    #     options.add_argument('--disable-gpu')
    #     options.add_argument('--disable-software-rasterizer')
    #     options.add_argument('--disable-background-timer-throttling')
    #     options.add_argument('--disable-backgrounding-occluded-windows')
    #     options.add_argument('--disable-renderer-backgrounding')
    #     options.add_argument('--disable-features=TranslateUI')
    #     options.add_argument('--disable-ipc-flooding-protection')
        
    #     # 메모리 최적화
    #     options.add_argument('--memory-pressure-off')
    #     options.add_argument('--max_old_space_size=2048')
    #     options.add_argument('--js-flags=--max-old-space-size=2048')
        
    #     # 네트워크 최적화
    #     options.add_argument('--disable-background-networking')
    #     options.add_argument('--disable-default-apps')
    #     options.add_argument('--disable-extensions')
    #     options.add_argument('--disable-sync')
        
    #     # 렌더링 최적화
    #     options.add_argument('--disable-images')
    #     options.add_argument('--disable-javascript')  # JS가 필요없다면
    #     options.add_argument('--disable-plugins')
        
    #     # 프로세스 관리
    #     options.add_argument('--single-process')  # 단일 프로세스 모드
    #     options.add_argument('--no-zygote')
        
    #     # 임시 디렉토리 설정
    #     self._tmp_profile = tempfile.mkdtemp(prefix='chrome_headless_')
    #     options.add_argument(f'--user-data-dir={self._tmp_profile}')
    #     options.add_argument(f'--data-path={self._tmp_profile}')
    #     options.add_argument(f'--disk-cache-dir={self._tmp_profile}')
        
    #     # 원격 디버깅 비활성화 (헤드리스에서는 불필요)
    #     options.add_argument('--remote-debugging-port=0')
    #     # opts.add_argument("--disable-blink-features=AutomationControlled")

    #     return options

    # def start_driver(self, headless: bool=False, retries: int=1):
    #     attempt = 0
    #     last_exc = None
    #     while attempt <= retries:
    #         try:
    #             chromedriver_autoinstall.install()
    #             options = self._build_options(headless)
    #             self.browser = Chrome(options=options)
    #             return  # 성공
    #         except SessionNotCreatedException as e:
    #             msg = str(e)
    #             last_exc = e
    #             # 현재 프로필 정리 후 재시도
    #             if self._tmp_profile:
    #                 shutil.rmtree(self._tmp_profile, ignore_errors=True)
    #                 self._tmp_profile = None
    #             if "user data directory is already in use" in msg and attempt < retries:
    #                 attempt += 1
    #                 continue
    #             raise  # 다른 원인이거나 재시도 소진
    #         except Exception as e:
    #             # 다른 예외
    #             # 실패해도 프로필 정리
    #             if self._tmp_profile:
    #                 shutil.rmtree(self._tmp_profile, ignore_errors=True)
    #                 self._tmp_profile = None
    #             raise
    #     if last_exc:
    #         raise last_exc


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
        return


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


class WinAdvancedStealthService:
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


class LinuxAdvancedStealthService:
    def __init__(self, stealth_config=None):
        self.stealth_config = stealth_config or {
            "languages": ["ko-KR", "ko", "en-US", "en"],  # 한국어 우선
            "vendor": "Google Inc.",
            "platform": "Linux x86_64",  # 리눅스 플랫폼
            "webgl_vendor": "Mesa",  # 리눅스 일반적인 WebGL 벤더
            "renderer": "llvmpipe (LLVM 12.0.1, 256 bits)",  # 리눅스 소프트웨어 렌더러
            "fix_hairline": True,
            "chrome_app": True,
            "chrome_csi": True,
            "chrome_load_times": True,
            "chrome_runtime": True,
            "iframe_content_window": True,
            "media_codecs": True,
            "navigator_permissions": True,
            "navigator_plugins": True,
            "navigator_webdriver": True,
            "outerdimensions": True,
            "hairline": True
        }

    def apply_stealth(self, browser):
        """스텔스 설정 적용"""
        try:
            from selenium_stealth import stealth
            self._apply_stealth_library(browser, self.stealth_config)
        except ImportError:
            print("selenium-stealth not installed, applying manual stealth")
        
        self._apply_additional_stealth(browser)
        self._apply_linux_specific_stealth(browser)

    def _apply_stealth_library(self, browser, stealth_config):
        """selenium-stealth 라이브러리 적용"""
        from selenium_stealth import stealth
        stealth(browser, **stealth_config)

    def _apply_additional_stealth(self, browser):
        """추가 스텔스 스크립트"""
        scripts = [
            # 웹드라이버 감지 방지
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
            
            # Chrome 런타임 객체 생성
            "window.navigator.chrome = {runtime: {}, loadTimes: function(){}, csi: function(){}};",
            
            # 언어 설정 (한국어 포함)
            "Object.defineProperty(navigator, 'languages', {get: () => ['ko-KR', 'ko', 'en-US', 'en']})",
            "Object.defineProperty(navigator, 'language', {get: () => 'ko-KR'})",
            
            # 플러그인 정보
            "Object.defineProperty(navigator, 'plugins', {get: () => Array.from({length: 5}, (_, i) => ({name: `Plugin ${i+1}`}))})",
            
            # 리눅스 플랫폼 정보
            "Object.defineProperty(navigator, 'platform', {get: () => 'Linux x86_64'})",
            "Object.defineProperty(navigator, 'userAgent', {get: () => navigator.userAgent.replace(/HeadlessChrome/, 'Chrome')})",
            
            # 하드웨어 정보 (리눅스 서버 환경)
            "Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 4})",
            "Object.defineProperty(navigator, 'deviceMemory', {get: () => 8})",
            
            # 권한 API
            """
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );
            """,
            
            # WebGL 정보 (리눅스 서버 환경)
            """
            const getParameter = WebGLRenderingContext.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Mesa';
                if (parameter === 37446) return 'llvmpipe (LLVM 12.0.1, 256 bits)';
                return getParameter(parameter);
            };
            """,
            
            # 배터리 API 제거 (서버 환경)
            "delete navigator.getBattery;",
            
            # 화면 정보 (일반적인 서버 해상도)
            "Object.defineProperty(screen, 'width', {get: () => 1920});",
            "Object.defineProperty(screen, 'height', {get: () => 1080});",
            "Object.defineProperty(screen, 'availWidth', {get: () => 1920});",
            "Object.defineProperty(screen, 'availHeight', {get: () => 1080});",
        ]

        for script in scripts:
            try:
                browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
            except Exception as e:
                print(f"Failed to execute stealth script: {e}")

    def _apply_linux_specific_stealth(self, browser):
        """리눅스 특화 스텔스 설정"""
        linux_scripts = [
            # 타임존 설정 (한국 시간)
            "Object.defineProperty(Intl.DateTimeFormat.prototype, 'resolvedOptions', {value: function(){return {timeZone: 'Asia/Seoul', locale: 'ko-KR'}}});",
            
            # 폰트 정보 (리눅스 일반 폰트)
            """
            Object.defineProperty(document, 'fonts', {
                get: () => ({
                    check: () => true,
                    ready: Promise.resolve(),
                    addEventListener: () => {},
                    removeEventListener: () => {}
                })
            });
            """,
            
            # 미디어 장치 정보
            """
            Object.defineProperty(navigator, 'mediaDevices', {
                get: () => ({
                    enumerateDevices: () => Promise.resolve([
                        {deviceId: 'default', kind: 'audioinput', label: 'Default - Built-in Microphone', groupId: 'group1'},
                        {deviceId: 'default', kind: 'audiooutput', label: 'Default - Built-in Speakers', groupId: 'group1'}
                    ]),
                    getUserMedia: () => Promise.reject(new Error('Permission denied'))
                })
            });
            """,
            
            # 연결 정보 (유선 연결)
            """
            Object.defineProperty(navigator, 'connection', {
                get: () => ({
                    effectiveType: '4g',
                    type: 'ethernet',
                    downlink: 10,
                    rtt: 50
                })
            });
            """,
        ]

        for script in linux_scripts:
            try:
                browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
            except Exception as e:
                print(f"Failed to execute Linux-specific stealth script: {e}")

class ChromeDriverService(WebDriverController):
    def __init__(self, args=None, paths=None, stealth_config=None):
        self.process_manager: ChromeProcessManager = ChromeProcessManager()
        if SYSTEM == 'Linux':
            self.stealth_manager: LinuxAdvancedStealthService = LinuxAdvancedStealthService(stealth_config)
        else:
            self.stealth_manager: WinAdvancedStealthService = WinAdvancedStealthService(stealth_config)
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