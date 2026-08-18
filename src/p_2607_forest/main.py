# CLI
import argparse, os, joblib
from p_2607_forest.config import MODEL_PATH, USER_ID, USER_PASSWORD
from p_2607_forest.core.get_url import get_url
from p_2607_forest.core.predict_imgbyte import predict_captcha_from_imgbyte
from p_2607_forest.utils.hardware_check_monitor import check_all_monitors_scaling
from p_2607_forest.utils.chrome_webdriver import ChromeBrowser

def main():
    # 1. CLI 실행
    ## 1) 인자 파서 생성
    parser = argparse.ArgumentParser(description="P_2607_FOREST '26.7 숲나들e 예약")
    ## 2) CLI 플래그 옵션 추가 (action="store_true"는 해당 옵션을 붙이면 True가 됨)
    parser.add_argument("--draw", action="store_true", help="🎰 추첨 신청")
    parser.add_argument("--first", action="store_true", help="🚀 선착순 예약")
    parser.add_argument("--month", action="store_true", help="🈷️ 월별 예약")
    ## 3) 입력된 인자 파싱
    args = parser.parse_args()
    ## 4) 입력된 인자에 따라 해당 함수 실행
    if args.draw:
        _TARGET_URL = get_url('draw')
    elif args.first:
        _TARGET_URL = get_url('first')
    elif args.month:
        _TARGET_URL = get_url('month')            
    else: # 옵션을 둘 다 안 적었을 경우 안내 메시지 출력
        print("\n❌ 실행 옵션을 입력해주세요.\n")
        parser.print_help()  # 도움말 출력    
        return    
    
    # 2. 모니터 배율(해상도) 점검 (배율 높은 경우, 캡챠 이미지 사이즈 변경됨)
    if not check_all_monitors_scaling():
        print("❌ 프로그램 중단 - 모니터 배율 100% 아님")
        return
    
    # 3. 메인 루프 진행
    print("======= 숲나들e 자동 추첨 신청 시스템 (무한루프 버전) =======")    
    if not os.path.exists(MODEL_PATH):
        print(os.path.abspath(MODEL_PATH))
        print(f"⚠️ 학습된 모델 파일({MODEL_PATH})이 존재하지 않습니다!")
        return        
    print("💾 머신러닝 최적화 모델 로딩 중...")
    model = joblib.load(MODEL_PATH)

    # 4. chrome_webdriver 실행
    driver = ChromeBrowser(headless=False, detach=True)    
    ## 대상 URL 접속      
    driver.go_page(_TARGET_URL)                
    
    # 5. 자동 로그인    
    driver.login_foresttrip(USER_ID, USER_PASSWORD)
        
    # 직접 로그인
    # print("💡 캡차 이미지가 완전히 로딩될 때까지 10초간 대기합니다...")
    # print("🆔 로그인 해주세요...")
    # time.sleep(10)     

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
                captcha_img = driver.get_captcha_image()
                img_bytes = captcha_img.screenshot_as_png
                
                pred_text = predict_captcha_from_imgbyte(model, img_bytes)
                if not pred_text:
                    print("❌ 캡차 이미지를 로드하는 데 실패했습니다. 다시 시도해 주세요.")
                    continue
                    
                print(f"🤖 AI 예측 결과 👉 [{pred_text}]")
                
                # 2) 캡챠입력 → 약관동의 → 신청클릭 → 알림창확인                
                driver.reservation_step(pred_text)
                           
                loop_count += 1
                
            except Exception as e:
                print(f"⚠️ 이번 시도 중 오류가 발생하여 건너뜁니다. (이유: {e})")
                print("💡 페이지 상태나 로그인 세션을 확인한 뒤 다시 엔터를 눌러주세요.")
                continue

    finally:
        print("🔒 웹 브라우저를 닫는 중...")
        driver.close()
        print("🏁 매크로 프로그램이 완전히 종료되었습니다.")

if __name__ == "__main__":
    main()