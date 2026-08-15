from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_chrome(headless: bool = False, detach: bool = True) -> webdriver.Chrome:
    """Chrome WebDriver를 생성하고 설정된 옵션을 적용하여 반환합니다.    
    1)headless
    False(기본값): 브라우저 화면에 출력, 개발/디버깅 목적
    True(옵션): 백그라운드 실행, 서버/성능 목적
    2)detach
    True(기본값): 코드 실행 후 브라우저 유지, 개발/디버깅 목적
    False(옵션): 코드 실행 후 브라우저 닫힘, 릴리즈/성능 목적
    3)return: 설정이 완료된 Chrome WebDriver 인스턴스
    """
    chrome_options = Options()
    # 창 크기 설정
    chrome_options.add_argument("--window-size=1300,1400")
    # Headless 모드 옵션 (필요 시 활성화 가능)
    if headless:
        chrome_options.add_argument("--headless=new")
    # 1. 자동화 표시 및 경고창 제거
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    # 2. 실행 완료 후 브라우저 유지 설정
    chrome_options.add_experimental_option("detach", detach)
    # 3. 비밀번호 저장 팝업 및 관리자 비활성화
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    # 4. 알림 팝업 차단 (필요 시 주석 해제)
    # chrome_options.add_argument("--disable-notifications")
    # 자동화 플래그 비활성화 (navigator.webdriver를 false/undefined로 처리)
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

if __name__ == "__main__":
    # 모듈 단독 테스트용 코드
    driver = create_chrome()
    driver.get("https://www.google.com")