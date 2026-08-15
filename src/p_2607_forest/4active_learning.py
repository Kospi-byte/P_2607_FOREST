import os, time, random
import joblib
from selenium.webdriver.common.by import By

from p_2607_forest.core.get_url import get_url
from p_2607_forest.core.predict_imgbyte import predict_captcha_from_imgbyte
from p_2607_forest.config import (
    IMG_LENGTH, MODEL_PATH,
    IMG_FOLDER_PATH, AUTO_DATA_TO_COLLECT
)
from p_2607_forest.utils.webdriver_chrome import create_chrome
from p_2607_forest.utils.webdriver_login import login_forest

_TOTAL_IMAGES_TO_COLLECT = AUTO_DATA_TO_COLLECT # 한 세션에 레이블링할 이미지 개수
_TARGET_URL = get_url('first')

# ==========================================
# 3. 실시간 액티브 러닝 코어 함수
# ==========================================
def active_learning_collector(target_url, count=10):
    os.makedirs(IMG_FOLDER_PATH, exist_ok=True)
    
    # 1) 가중치 모델 로드
    if not os.path.exists(MODEL_PATH):
        print(f"⚠️ 모델 파일({MODEL_PATH})이 없습니다. 빈 가중치 파일이라도 생성 후 진행하세요.")
        return
    print("💾 머신러닝 모델 로드 완료.")
    model = joblib.load(MODEL_PATH)    

    # 웹 브라우저(Chrome) 실행    
    driver = create_chrome()
    
    try:
        # 대상 URL 접속      
        driver.get(target_url)        
        # 60자가 넘으면 앞 60자만 보여주고 뒤에 ... 붙이기
        short_url = target_url[:60] + "..." if len(target_url) > 60 else target_url        
        print(f"🔗 접속 완료: {short_url}")        

        # 직접 로그인
        # print("💡 캡차 이미지가 완전히 로딩될 때까지 10초간 대기합니다...")
        # print("🆔 로그인 해주세요...")
        # time.sleep(10) 
        
        # 자동 로그인
        driver = login_forest(driver=driver)        
        
        print(f"\n🚀 실시간 반자동 레이블링 시작 (목표 수량: {count}개)...")
        print("=" * 70)
        print(" [방법] 예측이 맞으면 [Enter], 틀리면 [6자리 정답 입력], 종료하려면 [q]")
        print("=" * 70)
        
        success_count = 0
        loop_idx = 1
        
        while success_count < count:
            try:
                # 캡차 엘리먼트 가져오기 (메모리 처리, 디스크 저장 X)
                captcha_element = driver.find_element(By.ID, "captchaImg")                                
                img_bytes = captcha_element.screenshot_as_png
                # 캡챠 예측 
                pred_text = predict_captcha_from_imgbyte(model,img_bytes)
                
                # 사용자 인터랙션 인터페이스
                print(f"\n🔍 [시도 {loop_idx}] ------------------------------------")
                print(f"🤖 현재 캡차 이미지에 대한 모델 예측 👉 [{pred_text}]")
                user_input = input("정답입니까? (맞으면 [Enter] / 틀리면 [6자리 입력] / 종료 [q]): ").strip()
                
                if user_input.lower() == 'q':
                    print("\n👋 사용자가 작업을 중단했습니다.")
                    break
                
                # 정답 라벨 결정
                if user_input == "":
                    final_label = pred_text
                    print(f"✅ 예측 성공! [{final_label}] 데이터를 저장합니다.")
                else:
                    if len(user_input) != IMG_LENGTH or not user_input.isdigit():
                        print("❌ 입력 오류! 6자리 숫자만 입력 가능합니다. 현재 이미지는 건너뜁니다.")
                        driver.refresh()
                        time.sleep(2)
                        loop_idx += 1
                        continue
                    final_label = user_input
                    print(f"✍️ 수동 수정 완료! 오답 수정 결과 -> [{final_label}]")
                
                # 중복 파일명 방지 처리 및 저장
                file_path = os.path.join(IMG_FOLDER_PATH, f"{final_label}.png")
                if os.path.exists(file_path):
                    dup_count = 1
                    while os.path.exists(os.path.join(IMG_FOLDER_PATH, f"{final_label}_{dup_count}.png")):
                        dup_count += 1
                    file_path = os.path.join(IMG_FOLDER_PATH, f"{final_label}_{dup_count}.png")
                
                # 캡차 이미지 엘리먼트 파일로 최종 확정 저장
                captcha_element.screenshot(file_path)
                success_count += 1
                print(f"📸 학습 데이터 구축 완료 ({success_count}/{count}) -> {file_path}")
                
                # 다음 이미지 수집을 위한 웹페이지 새로고침 및 대기
                driver.refresh()
                loop_idx += 1
                time.sleep(random.randint(2, 4))
                
            except Exception as e:
                print(f"⚠️ 캡차 엘리먼트를 찾지 못했거나 오류 발생. 재시도 중... (로그인 상태 확인 요망)")
                driver.refresh()
                time.sleep(3)
                loop_idx += 1
                
    finally:
        driver.quit()
        print("\n==================================================")
        print(f"🎉 반자동 실시간 수집 완료! 총 {success_count}개의 데이터 추가.")
        print(f"📂 저장된 폴더: {os.path.abspath(IMG_FOLDER_PATH)}")
        print("💡 이제 기존 머신러닝 학습 코드를 돌려 모델 성능을 한 단계 올리세요!")
        print("==================================================")

if __name__ == "__main__":
    active_learning_collector(_TARGET_URL, count=_TOTAL_IMAGES_TO_COLLECT)