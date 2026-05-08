# 강의노트 자동화 시스템

신학대학원 1학기 5개 과목 강의노트 자동 정리 및 배포 시스템.

---

## 전체 흐름

```
수업 → 아이폰 녹취 → AirDrop → prepare.py 실행
  → Claude.ai에서 노트 생성 → HTML 저장
  → watch.py가 자동 감지 → 폴더 배치 + GitHub Pages 배포
```

---

## 처음 한 번만: 초기 설정

```bash
cd ~/Desktop/대학원/lecture-notes
python3 scripts/setup.py
```

- watchdog 라이브러리 자동 설치
- Claude.ai 과목별 프로젝트 URL 입력 (claude.ai → 프로젝트 클릭 → 주소창 URL 복사)

---

## 매주 사용법

### 1단계 — 감시 시작 (터미널 창 하나 띄워두기)

```bash
cd ~/Desktop/대학원/lecture-notes
python3 scripts/watch.py
```

> 맥북 켤 때 자동 시작하려면: `bash scripts/launch_watch.sh --install`

---

### 2단계 — 수업 후 준비 (prepare.py)

```bash
python3 scripts/prepare.py
```

자동으로:
1. Downloads에서 녹취 .txt 파일 감지
2. 과목 자동 추론 (또는 직접 선택)
3. 해당 과목 강의자료 목록 출력
4. Claude.ai 프로젝트 브라우저에서 자동 오픈
5. 녹취 파일 → `1학기/[과목]/녹취/` 이동

---

### 3단계 — Claude.ai에서 노트 생성 (수동)

브라우저에서 자동으로 열린 프로젝트에:
- 녹취 스크립트 (.txt) 업로드
- 해당 주차 강의자료 (PPT/PDF) 업로드
- 노트 생성 요청
- 결과 HTML → **아래 폴더에 저장** (Downloads 아님!)

```
~/Desktop/대학원/lecture-notes/input/
```

---

### 4단계 — 자동 처리 (watch.py가 알아서)

`input/` 폴더에 HTML 파일이 저장되면 macOS 다이얼로그가 뜸:
1. 과목 선택
2. 주차 입력 (다음 주차 자동 제안, 추가자료면 숫자+b: 예 `10b`)

이후 자동으로:
- `1학기/[과목]/노트/` — 원본 파일명으로 저장
- `lecture-notes/output/[과목]/weekNN.html` — 주차 파일명으로 저장
- data.js 업데이트 + git push → GitHub Pages 배포
- macOS 알림

---

## 폴더 구조

```
대학원/
  1학기/
    [과목]/
      강의자료/   ← 교수 제공 PPT, PDF (Claude.ai 업로드용)
      녹취/       ← 아이폰 녹취 스크립트 .txt
      노트/       ← 생성된 수업정리 HTML (원본명)
      과제/       ← 과제 파일
      _설정/      ← Claude.ai guidelines, 강의계획서
  lecture-notes/
    output/
      [과목]/     ← weekNN.html 형식 (GitHub Pages 배포본)
    scripts/
      config.json     ← 과목별 URL·경로 설정
      setup.py        ← 초기 설정 (최초 1회)
      prepare.py      ← 수업 후 준비
      watch.py        ← 자동 감시·배포
      launch_watch.sh ← 터미널 실행 / launchd 등록
      deploy.py       ← 수동 배포 (단독 사용 가능)
```

---

## 수동 배포 (watch.py 없이)

HTML 파일을 직접 output 폴더에 넣은 후:

```bash
python3 scripts/deploy.py [과목명] [주차] [날짜(선택)]

# 예시
python3 scripts/deploy.py 기독교철학 07 2026.04.16
python3 scripts/deploy.py 기독교철학 07b          # 추가자료
python3 scripts/deploy.py 신약성서I 09            # 오늘 날짜 자동
```

---

## 설정 변경

`scripts/config.json` 직접 편집 또는:

```bash
python3 scripts/setup.py   # URL 재입력, 경로 확인
```

---

## 문제 해결

| 증상 | 해결 |
|---|---|
| `watchdog 미설치` 오류 | `pip install watchdog` |
| URL 설정 안 됨 | `python3 scripts/setup.py` 재실행 |
| HTML 감지 안 됨 | 파일이 5KB 이상인지 확인, watch.py 실행 중인지 확인 |
| 배포 실패 | `cd lecture-notes && git status` 로 git 상태 확인 |
| launchd 로그 확인 | `tail -f ~/Library/Logs/lecture-watch.log` |
