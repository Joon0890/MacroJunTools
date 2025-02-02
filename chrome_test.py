from modules.utiles.chromedriver.chrome_manager import ChromeDriverManager
import socket
import pickle

if __name__ == "__main__":
    try:
        def find_available_port():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', 0))  # OS가 사용 가능한 포트를 자동 할당
                return s.getsockname()[1]
        
        available_port = find_available_port()

        print(f"사용 가능한 포트: {available_port}")

        manager = ChromeDriverManager()
        manager.start(headless=False, url="https://everytime.kr/")
            
        input("Press Enter to stop...")  # 테스트용

    except KeyboardInterrupt:
        print("User interrupted execution. Stopping ChromeDriverManager.")
    except Exception as e:
        print("Unexpected error: %s", e)
    finally:
        manager.stop()
        
