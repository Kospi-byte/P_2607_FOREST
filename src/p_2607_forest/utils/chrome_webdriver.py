"""
# .env
## .env (GitHub 업로드 제외)
## Environment file (.gitignore)
## .env
## .env.*
## !.env.example
# ----------------------------------
# 1. 글로벌 설정 값
# ----------------------------------
## URL
URL = "https://www.foresttrip.go.kr/pot/login/login.do"
## ID / PW
USER_ID="bklove9997"
USER_PASSWORD="asdqwe123!"
"""

"""
# config.py
## 3. 타입 변환 헬퍼 함수
## 2. 추가 필요 항목 정의 (경로 등)
## 1. 글로벌 설정 값 (.env)
# ----------------------------------
# 3. 타입 변환 헬퍼 함수 
# ----------------------------------
# int/str/float/bool 등
# NoneType/ValueError 방지 목적
import os
def _get_env_int(key: str, default: int = 0) -> int:
    val = os.getenv(key)
    try:
        return int(val) if val is not None else default
    except (ValueError, TypeError):
        return default
def _get_env_str(key: str, default: str = "") -> str:
    return os.getenv(key, default)
def _get_float(key: str, default: float = 0.0) -> float:
    val = os.getenv(key)
    try:
        return float(val) if val is not None else default
    except (ValueError, TypeError):
        return default
# ----------------------------------
# 2. 추가 필요 항목 정의 
# ----------------------------------
# 프로젝트 루트 = BASE_DIR
# 현재파일 기준 부모/부모 폴더
import pathlib
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
_ENV_PATH = BASE_DIR / ".env"
# ----------------------------------
# 1. 글로벌 설정 값 (.env)
# ----------------------------------
# .env 의 모든 항목 가져오기
# 글로벌 상수 추가
import dotenv
dotenv.load_dotenv(dotenv_path=_ENV_PATH)
## [.env]
URL = _get_env_str("URL", "https://www.google.com/")
## ID / PW
USER_ID=_get_env_str("USER_ID", "dafault_id")
USER_PASSWORD=_get_env_str("USER_PASSWORD", "dafault_pw")
"""

"""
# main.py
from project.utils.chrome_webdriver import ChromeBrowser
from project.config import (URL, USER_ID, USER_PASSWORD)
# 1. URL
LOGIN_URL = URL
# 2. 브라우저 객체 생성
browser = ChromeBrowser(headless=False, detach=True)
try:
    # 3. 페이지 이동
    browser.go_page(LOGIN_URL)
    # 4. 숲나들e 로그인 수행 (ID, PW만 전달)
    browser.login_foresttrip(user_id=USER_ID, user_pw=USER_PASSWORD)
    # 추가 작업 수행 (예: 예약 페이지 이동 등)
    # ...
except Exception as e:
    print(f"실행 중 예기치 않은 오류 발생: {e}")
"""

# utils_module_code.py
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChromeBrowser:
    """Chrome WebDriver 제어 클래스

    **headless**
    * False(기본값): 브라우저 화면에 출력, 개발/디버깅 목적
    * True(옵션): 백그라운드 실행, 서버/성능 목적

    **detach**
    * True(기본값): 코드 실행 후 브라우저 유지, 개발/디버깅 목적
    * False(옵션): 코드 실행 후 브라우저 닫힘, 릴리즈/성능 목적
    """

    def __init__(self, headless: bool = False, detach: bool = True):
        self.headless = headless
        self.detach = detach
        self.driver = self._open_chrome()


    def _open_chrome(self) -> webdriver.Chrome:
        """Chrome WebDriver를 열고 설정된 옵션을 적용하여 반환합니다."""
        chrome_options = Options()
        # 창 크기 설정
        chrome_options.add_argument("--window-size=1300,1400")
        
        # headless 모드 옵션 (argument headless)
        if self.headless:
            chrome_options.add_argument("--headless=new")
            
        # 1. 자동화 표시 및 경고창 제거
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # 2. 실행 완료 후 브라우저 유지 설정 (argument detach)
        chrome_options.add_experimental_option("detach", self.detach)
        
        # 3. 비밀번호 저장 팝업 및 관리자 비활성화
        prefs = {"credentials_enable_service": False,
            "profile.password_manager_enabled": False,}
        chrome_options.add_experimental_option("prefs", prefs)
        
        # 4. 자동화 플래그 비활성화
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        # 5. User-Agent 설정
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        chrome_options.add_argument(f"user-agent={user_agent}")

        print("🌐 크롬 브라우저를 시작하는 중...")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def go_page(self, url: str) -> None:
        """지정된 URL로 이동합니다."""
        self.driver.get(url)
        # 60자가 넘으면 앞 60자만 보여주고 뒤에 ... 붙이기
        short_url = url[:60] + "..." if len(url) > 60 else url        
        time.sleep(1)
        print(f"🔗 접속 완료: {short_url}")

    def login_foresttrip(self, user_id: str, user_pw: str) -> None:
        """
        숲나들e 전용 로그인 함수.
        화면 요소(XPath)는 내부에 고정하고, ID와 PW만 인자로 받습니다.
        """
        print(f"🆔 숲나들e 로그인 시도 중... (ID: {user_id})")        
        # 숲나들e 전용 XPath 고정값
        id_xpath = '//*[@id="mmberId"]'
        pw_xpath = '//*[@id="gnrlMmberPssrd"]'
        btn_xpath = '//*[@id="infoWrap"]/fieldset/div/div[2]/input[3]'

        try:
            # 1. 아이디 입력
            id_input = self.driver.find_element(By.XPATH, id_xpath)
            id_input.clear()
            id_input.send_keys(user_id)

            # 2. 비밀번호 입력
            pw_input = self.driver.find_element(By.XPATH, pw_xpath)
            pw_input.clear()
            pw_input.send_keys(user_pw)

            # 3. 로그인 버튼 클릭
            login_btn = self.driver.find_element(By.XPATH, btn_xpath)
            login_btn.click()
            time.sleep(0.5)

            # 4. 오류 알림창 확인
            try:
                alert = self.driver.switch_to.alert
                print(f"❌ 숲나들e 로그인 실패 (알림창): {alert.text}")
                alert.accept()
            except NoAlertPresentException:
                print("✅ 숲나들e 로그인 완료")
                
        except WebDriverException as e:
            print(f"❌ 요소찾기 또는 버튼클릭 실패: {e}")
            
    def get_captcha_image(self):
        """
        캡차 이미지 웹 요소를 찾아서 반환하는 함수
        """
        print("🔍 캡차 이미지 요소 탐색 중...")
        captcha_element = self.driver.find_element(By.ID, "captchaImg")        
        return captcha_element
    
    def reservation_step(self, pred_text: str) -> None:
        """
        캡챠입력 → 약관동의 → 신청클릭 → 알림창확인
        화면 요소(ID, CSS)는 내부에 고정하고, 캡챠 예측 텍스트만 인자로 받습니다.
        """
        print(f"📝 예약 단계 진행 중... (입력할 캡차: {pred_text})")        
        # 숲나들e 예약 전용 고정값
        captcha_id = "atmtcRsrvtPrvntChrct"
        agree_css = "#chkAgree, #arr_01"
        submit_css = "#btnRsrvt, #btnRsrvtSave"
        
        try:
            # 1. 캡차 입력
            captcha_input = self.driver.find_element(By.ID, captcha_id)
            captcha_input.clear()
            captcha_input.send_keys(pred_text)            
            # 2. 약관 동의 체크
            agree_checkbox = self.driver.find_element(By.CSS_SELECTOR, agree_css)
            if not agree_checkbox.is_selected():
                agree_checkbox.click()                
            # 3. 신청 버튼 클릭    
            submit_button = self.driver.find_element(By.CSS_SELECTOR, submit_css)    
            submit_button.click()
            print("🔘 정보 입력 및 신청 버튼 클릭 완료.")            
            # 4. 알림창 확인
            print("⏳ 브라우저 알림창 탐지 중...")
            try:
                # 2초 대기하며 알림창을 찾음
                WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                print(f"💬 알림창 내용: [{alert.text}]")
                alert.accept()
                print("✅ 알림창 [확인] 클릭 완료!")
            except TimeoutException:
                # 2초 동안 알림창이 뜨지 않았을 경우 (에러 없이 패스)
                print("✅ 알림창이 나타나지 않았습니다. (정상 진행)")
                
        except WebDriverException as e:
            # 요소를 찾을 수 없거나 클릭할 수 없는 등 셀레니움 관련 에러 발생 시
            print(f"❌ 요소찾기 또는 버튼클릭 실패: {e}")    
    
    def close(self) -> None:
        """Chrome WebDriver 브라우저 종료"""
        print("🛑 브라우저를 종료합니다.")
        self.driver.quit()        
        
if __name__ == "__main__":
    # 모듈 단독 실행 코드
    print("▶️ 모듈 단독 실행 테스트를 시작합니다.")
    
    # 1. 브라우저 객체 생성 (화면 표시, 종료 후 유지 옵션)
    browser = ChromeBrowser(headless=False, detach=True)
    
    # 2. 구글로 이동 테스트
    browser.go_page("https://www.foresttrip.go.kr/com/login.do?hmpgId=FRIP&menuId=007003&targetUrl=/main.do?hmpgId=FRIP")   
    browser.login_foresttrip(user_id='abcd', user_pw='1234')
    
    print("✅ 숲나들e 접속 테스트 완료")