# config.py
## 1. .env 의 모든 항목 가져오기
## 2. 추가 필요 항목 정의 (경로 등)
## 3. 타입 변환 헬퍼 함수

import os
from pathlib import Path
import dotenv

# ----------------------------
# 2. 추가 필요 항목 정의 (경로 등)
# ----------------------------
# 1. 프로젝트 루트 경로 및 .env 파일 위치 자동 탐색
# (현재 파일 기준 부모/부모 폴더 = 프로젝트 최상위 루트)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
_ENV_PATH = BASE_DIR / ".env"
dotenv.load_dotenv(dotenv_path=_ENV_PATH)
# [경로 관련 설정]
IMG_FOLDER_PATH = BASE_DIR / "data" / "learning"
MODEL_FOLDER_PATH = BASE_DIR / "src" / "p_2607_forest" / "model"
MODEL_PATH = BASE_DIR / "src" / "p_2607_forest" / "model" / "captcha_ml_model.pkl"

# 1collect.py 학습데이터 수집하기
TOTAL_IMAGES_TO_COLLECT = 5
# 4active_learning.py 반자동 데이터 레이블링
AUTO_DATA_TO_COLLECT = 5

# -------------------------------------------------------------
# 3. 안전한 타입 변환 헬퍼 함수들 (NoneType / ValueError 방지용)
# -------------------------------------------------------------
def get_env_int(key: str, default: int = 0) -> int:
    val = os.getenv(key)
    try:
        return int(val) if val is not None else default
    except (ValueError, TypeError):
        return default

def get_env_str(key: str, default: str = "") -> str:
    return os.getenv(key, default)

# def _get_float(key: str, default: float = 0.0) -> float:
#     val = os.getenv(key)
#     try:
#         return float(val) if val is not None else default
#     except (ValueError, TypeError):
#         return default

# def _get_bool(key: str, default: bool = False) -> bool:
#     val = os.getenv(key)
#     if val is None:
#         return default
#     return val.strip().lower() in ("true", "1", "yes")

# ------------------------
# 1. 글로벌 설정 값 (.env)
# ------------------------
# 1. 숲나들e URL
## 추첨 신청 (월 추첨)
## 선착순 예약 (청도자연휴양림 D+30)
## 월별현황 조회
DRAW_URL = get_env_str("DRAW_URL", "www.google.com")
FIRST_URL = get_env_str("FIRST_URL", "www.google.com")
MONTH_URL = get_env_str("MONTH_URL", "www.google.com")

# 2. 글로벌 설정 값 (데이터 그림파일, 여백 제거, 폴더 경로)
## 학습데이터 그림파일 크기
IMG_WIDTH = get_env_int("IMG_WIDTH", 130)
IMG_HEIGHT = get_env_int("IMG_HEIGHT", 35)
## 학습데이터 그림파일 내 숫자 파트
DEL_WIDTH_L = get_env_int("DEL_WIDTH_L", 8) # 좌여백 제거량
DEL_WIDTH_R = get_env_int("DEL_WIDTH_R", 14) # 우여백 제거량
DEL_WIDTH_B = get_env_int("DEL_WIDTH_B", 9) # 하여백 제거량
COUNT_OF_NUMBER = get_env_int("COUNT_OF_NUMBER", 6) # 글자수
### [추가] - 이미지 전처리 및 학습 관련 설정
NUMBER_WIDTH_L = DEL_WIDTH_L # 숫자가 시작하는 픽셀 (좌여백 제거용)
NUMBER_WIDTH_R = IMG_WIDTH - DEL_WIDTH_R # 숫자가 끝나는 픽셀 (우여백 제거용)
NUMBER_WIDTH = NUMBER_WIDTH_R - NUMBER_WIDTH_L # IMG_LENGTH = 6 나누기 위해 6의 배수 맞춤
NUMBER_HEIGHT = IMG_HEIGHT - DEL_WIDTH_B # (하여백 제거용)
IMG_LENGTH = COUNT_OF_NUMBER # 글자수

# 3. ID / PW
USER_ID = get_env_str("USER_ID", "default_id")
USER_PASSWORD = get_env_str("USER_PASSWORD", "default_pw")
# USER_ID = os.getenv("USER_ID", "default_user")
# USER_PASSWORD = os.getenv("USER_PASSWORD", "default_pw")