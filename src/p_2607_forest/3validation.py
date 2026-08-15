from pathlib import Path
import cv2
import numpy as np
import joblib

from p_2607_forest.config import (
    BASE_DIR,
    IMG_WIDTH, IMG_HEIGHT,
    NUMBER_WIDTH_L, NUMBER_WIDTH_R,
    NUMBER_WIDTH, NUMBER_HEIGHT,
    IMG_LENGTH, MODEL_PATH
)

def main():
    # 1. 10개 샘플에 대한 실제 정답 리스트 (문자열 형태로 입력)
    ground_truth = [
        "594823",  # target_001.png
        "684548",  # target_002.png
        "572696",  # target_003.png
        "062923",  # target_004.png
        "290909",  # target_005.png
        "933998",  # target_006.png
        "985246",  # target_007.png
        "158557",  # target_008.png
        "115972",  # target_009.png
        "908501",  # target_010.png
    ]
    correct_count = 0
    total_evaluated = 0

    # target 폴더 기준 경로 설정 (BASE_DIR / "data" / "target")
    _target_dir = BASE_DIR / "data" / "target"

    # 2. 1부터 10까지 반복 검증
    for i in range(1, 11):
        # target_path = f"../../data/target/target_{i:03d}.png"
        _target_path = _target_dir / f"target_{i:03d}.png"
        actual_label = ground_truth[i - 1]  # 0번 인덱스부터 매칭

        try:
            # 예측값 가져오기 (문자열 타입 및 공백 제거 처리)
            pred = str(result_img(_target_path)).strip()
            total_evaluated += 1
            # 정답 비교
            if pred == actual_label:
                is_correct = "O"
                correct_count += 1
            else:
                is_correct = "X"                        
            print(
                f"[{_target_path.name}] 예측값: {pred} (정답: {actual_label}) {is_correct}"
            )

        except FileNotFoundError as e:
            print(f"Error processing {_target_path}: {e}")

    # 3. 전체 정답률 계산 및 출력
    if total_evaluated > 0:
        accuracy = (correct_count / total_evaluated) * 100
        print(
            f"\n✅ 정답률 {accuracy:.1f} % ({correct_count}/{total_evaluated})"
        )
    else:
        print("\n평가된 파일이 없습니다.")            
            
# 캡차 이미지를 문자 단위로 균등하게 6등분하여 자르고 데이터화하는 함수
def preprocess_captcha(img_path):
    # 흑백 이미지로 읽기
    # img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"⚠️ 이미지를 찾을 수 없습니다: {img_path}")
    
    # 이미지 크기 강제 고정
    img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
    
    # 이미 (좌우하) 여백 제거 (숫자만 남김)
    img = img[:NUMBER_HEIGHT, NUMBER_WIDTH_L : NUMBER_WIDTH_R]
    
    # 픽셀 값 정규화 (0~1 사이)
    img = img.astype(np.float32) / 255.0
    
    # 가로 길이를 글자 수(6)만큼 등분하여 슬라이싱    
    char_width = NUMBER_WIDTH // IMG_LENGTH
    char_images = []
    
    for i in range(IMG_LENGTH):
        start_x = i * char_width
        end_x = start_x + char_width
        char_img = img[:, start_x:end_x]
        
        # 최신 머신러닝 입력용으로 2차원 이미지를 1차원 배열(픽셀 피처)로 평탄화(Flatten)
        char_images.append(char_img.flatten())
        
    return np.array(char_images)

# [가중치로 결과 도출] 저장된 모델로 텍스트 예측
def result_img(img_path):    
    _target_img_path = Path(img_path)
    
    # Path 객체의 .exists() 메서드로 파일 존재 여부 확인
    if not Path(MODEL_PATH).exists():
        raise FileNotFoundError(f"⚠️ 학습된 모델 파일({MODEL_PATH})이 없습니다! learn_img()를 먼저 실행해 주세요.")
    if not _target_img_path.exists():
        raise FileNotFoundError(f"⚠️ 타겟 이미지 파일({_target_img_path})이 존재하지 않습니다.")

    # 저장된 머신러닝 모델 로드    
    model = joblib.load(MODEL_PATH)
    
    # 타겟 이미지 슬라이싱 및 전처리
    char_features = preprocess_captcha(_target_img_path)
    
    # 6개 글자 각각 예측 수행
    predictions = model.predict(char_features)
    
    # 문자 리스트를 하나의 문자열로 결합하여 반환
    return "".join(predictions)

if __name__ == "__main__":
    main()