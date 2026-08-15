# CLI
import argparse
import os
import joblib
from selenium.webdriver.common.by import By

from p_2607_forest.config import BASE_DIR
from p_2607_forest.core.make_url import get_url
from p_2607_forest.core.image_utils import predict_captcha
from p_2607_forest.core.web_utils import process_reservation_step

from p_2607_forest.utils.webdriver_chrome import create_chrome
from p_2607_forest.utils.webdriver_login import login_forest

# 현재 파일(main.py)이 있는 폴더 기준 -> model/captcha_ml_model.pkl
# BASE_DIR = Path(__file__).resolve().parent
_MODEL_PATH = BASE_DIR / "src" / "p_2607_forest" / "model" / "captcha_ml_model.pkl"

def main():
    # 1. 인자 파서 생성
    parser = argparse.ArgumentParser(description="P_2606_FOREST CLI 실행 프로그램")

    # 2. CLI 플래그 옵션 추가 (action="store_true"는 해당 옵션을 붙이면 True가 됨)
    parser.add_argument("--draw", action="store_true", help="🎰 추첨 신청")
    parser.add_argument("--first", action="store_true", help="🚀 선착순 예약")

    # 3. 입력된 인자 파싱
    args = parser.parse_args()

    # 4. 입력된 인자에 따라 해당 함수 실행
    if args.draw:
        _TARGET_URL = get_url('draw')
    if args.first:
        _TARGET_URL = get_url('first')
    # 옵션을 둘 다 안 적었을 경우 안내 메시지 출력
    if not args.draw and not args.first:
        print("⚠️ 실행할 옵션을 입력해주세요.")
        parser.print_help()  # 도움말 출력    
        return
    
    # 2. 메인 루프 진행
    print("======= 숲나들e 자동 추첨 신청 시스템 (무한루프 버전) =======")    
    if not os.path.exists(_MODEL_PATH):
        print(os.path.abspath(_MODEL_PATH))
        print(f"⚠️ 학습된 모델 파일({_MODEL_PATH})이 존재하지 않습니다!")
        return
        
    print("💾 머신러닝 최적화 모델 로딩 중...")
    model = joblib.load(_MODEL_PATH)

    # 웹 브라우저(Chrome) 실행    
    driver = create_chrome()    
    
    # 대상 URL 접속      
    driver.get(_TARGET_URL)        
    # 60자가 넘으면 앞 60자만 보여주고 뒤에 ... 붙이기
    short_url = _TARGET_URL[:60] + "..." if len(_TARGET_URL) > 60 else _TARGET_URL        
    print(f"🔗 접속 완료: {short_url}")        

    # 직접 로그인
    # print("💡 캡차 이미지가 완전히 로딩될 때까지 10초간 대기합니다...")
    # print("🆔 로그인 해주세요...")
    # time.sleep(10) 
    
    # 자동 로그인
    driver = login_forest(driver=driver)    

    try:    
        loop_count = 1
        
        # 무한 루프 시작
        while True:
            print("\n" + "-" * 50)
            print(f"🔄 [{loop_count}회] 매크로 대기 중...")
            print("🔹 [Enter]     : 즉시 캡차 풀고 자동 신청 진행")
            print("🔹 [q + Enter] : 프로그램 안전하게 종료")
            print("-" * 50)
            
            user_command = input("👉 명령을 입력하세요: ").strip().lower()
            
            if user_command == 'q':
                print("\n👋 사용자가 종료를 요청했습니다. 프로그램을 안전하게 종료합니다.")
                break
                
            print("\n🚀 자동 신청 시퀀스 즉시 가동!")
            
            try:
                # 1) 캡차 스크린샷 및 모델 예측
                captcha_element = driver.find_element(By.ID, "captchaImg")
                img_bytes = captcha_element.screenshot_as_png
                
                pred_text = predict_captcha(model, img_bytes)
                if not pred_text:
                    print("❌ 캡차 이미지를 로드하는 데 실패했습니다. 다시 시도해 주세요.")
                    continue
                    
                print(f"🤖 AI 예측 결과 👉 [{pred_text}]")
                
                # 2) 폼 입력, 동의, 클릭, 알림창 확인 자동 수행
                process_reservation_step(driver, pred_text)
                
                loop_count += 1
                
            except Exception as e:
                print(f"⚠️ 이번 시도 중 오류가 발생하여 건너뜁니다. (이유: {e})")
                print("💡 페이지 상태나 로그인 세션을 확인한 뒤 다시 엔터를 눌러주세요.")
                continue

    finally:
        print("🔒 웹 브라우저를 닫는 중...")
        driver.quit()
        print("🏁 매크로 프로그램이 완전히 종료되었습니다.")

if __name__ == "__main__":
    main()