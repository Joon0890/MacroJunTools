# # # test_step1.py

# # from selenium import webdriver
# # from selenium.webdriver.chrome.service import Service as ChromeService
import chromedriver_autoinstaller

# # try:
# #     print("가장 기본적인 Selenium 실행 테스트를 시작합니다...")
driver_path = chromedriver_autoinstaller.install()
# #     # webdriver-manager를 사용해 자동으로 드라이버 설정
# #     driver = webdriver.Chrome()
    
# #     driver.get("https://www.google.com")
# #     print("Google 페이지 접속 성공!")
    
# #     driver.quit()
# #     print("테스트 성공적으로 완료.")

# # except Exception as e:
# #     print(f"1단계 테스트 실패: {e}")


# """
# (every) C:\Users\USER\joonspace\MacroJunTools>python 111.py
# 가장 기본적인 Selenium 실행 테스트를 시작합니다...

# DevTools listening on ws://127.0.0.1:64804/devtools/browser/13912377-2d56-4fa7-942c-9947e4bf756b
# Google 페이지 접속 성공!
# 테스트 성공적으로 완료.
# """


# """
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
# 이것도 올바르게 실행됨
# """

# test_step2.py

from selenium import webdriver
from subprocess import Popen
from selenium.webdriver.chrome.service import Service


try:
    print("debuggerAddress 연결 테스트를 시작합니다...")
    service = Service(executable_path=driver_path)

    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    # 이 코드가 실행되면, 이미 열려있는 Chrome 창의 주소가 naver.com으로 바뀝니다.
    driver.get("https://www.naver.com")
    print("Naver 페이지 접속 성공!")
    
    # 이 테스트에서는 quit()를 호출하지 않습니다. 브라우저를 직접 닫아주세요.
    print("테스트 성공. 터미널과 브라우저를 직접 닫아주세요.")

except Exception as e:
    print(f"2단계 테스트 실패: {e}")