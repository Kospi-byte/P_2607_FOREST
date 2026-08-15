from p_2607_forest.config import USER_ID, USER_PASSWORD
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, WebDriverException

def print_credentials() -> None:
    """ID와 Password를 출력하는 함수"""
    print("=== [계정 정보 확인] ===")
    print(f"ID       : {USER_ID}")
    print(f"Password : {USER_PASSWORD}")

def login_forest(driver: webdriver.Chrome) -> webdriver.Chrome:
    """
    숲나들e 로그인 페이지에서 ID/PW 입력하고 로그인 버튼을 클릭    
    """
    print("🆔 자동 로그인 중... ")
    # 1. 아이디 입력
    id_input = driver.find_element(By.XPATH, '//*[@id="mmberId"]')
    id_input.clear()
    id_input.send_keys(USER_ID)

    # 2. 비밀번호 입력
    pw_input = driver.find_element(By.XPATH, '//*[@id="gnrlMmberPssrd"]')
    pw_input.clear()
    pw_input.send_keys(USER_PASSWORD)

    # 3. 로그인 클릭
    try:
        # 로그인 버튼 클릭
        login_btn = driver.find_element(
            By.XPATH, '//*[@id="infoWrap"]/fieldset/div/div[2]/input[3]'
        )
        login_btn.click()
        time.sleep(0.5)
        # 오류 알림창(비밀번호 불일치 등)이 떴는지 확인
        try:
            alert = driver.switch_to.alert
            print(f"❌ 로그인 실패 (알림 메시지): {alert.text}")
            alert.accept()  # 알림창 닫기
        except NoAlertPresentException:
            # 알림창이 없다면 정상 로그인 완료
            print("✅ 로그인 성공...")
    except WebDriverException as e:
        print(f"❌ 버튼클릭 실패: {e}")
   
    return driver

if __name__ == "__main__":
    # 단독 실행 시 바로 출력
    print_credentials()