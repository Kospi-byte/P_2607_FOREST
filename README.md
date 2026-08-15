# 웹 자동화 - 숲나들e 예약 캡챠   
## 배경
- '26년6월 개발 버전
- '26년7월 릴리즈 버전
- [머신런닝을 이용한 자동방지 문자 캡챠 뚫어보기](https://gam860720.tistory.com/532) 블로그를 보고 시작   
## 사용법
1. collect.py 학습데이터 수집하기
    - TOTAL_IMAGES_TO_COLLECT 는 config.py 수정
    - 접속가능 URL 찾는법 - 숲나들e 메인에서 추첨신청 or 일반예약
    - 추첨신청은 안되는 기간이 있어서 그때는 일반예약
    - 자동로그인 (수동 전환 가능)
2. learning.py 학습하기
3. validation.py 검증하기
    - data/target 데이터로 성능검증
    - 10개로 검증 (target_001 ~ target_010)
4. active_learning.py 반자동 데이터 레이블링
    - AUTO_DATA_TO_COLLECT 는 config.py 수정
    - 자동로그인 (수동 전환 가능)
5. main.py 작동시키기
    --draw      🎰 추첨 신청
    --first     🚀 선착순 예약
    - 추첨신청 close 시, 일반예약 시도

## 기타
[x] old/learning.py & main.py 는 데이터 그림 전체 (130*35) 로 학습과 실행   
[x] 성능 저하 이슈로 배경은 삭제하고 숫자 영역만 사용하는 코드로 변경
[x] 1: release version
[x] 2: core filename change