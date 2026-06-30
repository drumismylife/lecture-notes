# 강의노트 자동화 시스템

---

## ① 최초 1회 설정

### 1. 의존성 설치 + Claude.ai URL 등록
```bash
cd ~/Desktop/대학원/lecture-notes
python3 scripts/setup.py
```
- 각 과목의 Claude.ai 프로젝트 URL 입력
- URL 찾는 법: claude.ai → 왼쪽 사이드바 프로젝트 클릭 → 주소창 URL 복사

### 2. 감시 앱 Dock에 추가
```bash
bash apply_icon.sh
```
완료 후 Finder에서 `강의노트 감시.app`을 Dock으로 드래그

### 3. TextEdit 기본 형식 변경 (RTF 방지)
`TextEdit → 설정(⌘,) → 포맷 → 일반 텍스트` 선택

---

## ② 매주 수업 후 — 단계별 실행

### STEP 1 | 감시 시작
Dock의 **🦉 강의노트 감시 앱** 클릭
→ 터미널 창이 열리고 감시 시작 (이 창은 열어둔 채로)

---

### STEP 2 | 녹취 전사문 저장 + 준비
아이폰에서 전사문 **복사** 후, 맥북 터미널에서:

```bash
pbpaste > ~/Downloads/녹취_신약성서_5월7일_누가복음마지막.txt && python3 ~/Desktop/대학원/lecture-notes/scripts/prepare.py
```

자동으로 진행되는 것들:
- 클립보드 내용을 날짜 파일명으로 Downloads에 저장 (예: `녹취_0508.txt`)
- 과목 자동 감지 → 확인 또는 번호로 선택
- 해당 과목 강의자료 목록 출력
- Claude.ai 해당 과목 프로젝트 브라우저 자동 오픈
- 녹취 파일 → `1학기/[과목]/녹취/` 자동 이동

---

### STEP 3 | Claude.ai에서 노트 생성 (수동)
자동으로 열린 프로젝트에서:
1. 녹취 `.txt` 파일 업로드
2. 해당 주차 강의자료 PPT/PDF 업로드
3. 노트 생성 요청
4. 완성된 HTML을 **아래 폴더에 저장:**

```
~/Desktop/대학원/lecture-notes/input/
```

> ⚠️ Downloads가 아닌 반드시 `input/` 폴더에 저장해야 자동 감지됩니다

---

### STEP 4 | 자동 처리 (watch.py가 알아서)
`input/` 폴더에 HTML이 저장되면 자동으로:
1. macOS 팝업 → 과목 선택
2. 주차 입력 (다음 주차 자동 제안, 추가자료면 숫자+b: 예 `10b`)
3. `1학기/[과목]/노트/` 저장 (원본 파일명)
4. `output/[과목]/week10.html` 저장
5. GitHub Pages 자동 배포
6. 완료 알림 🔔
7. 원본 → `input/done/` 자동 이동

---

## ③ 전체 흐름 요약

```
🦉 감시 앱 클릭 (watch.py 시작)
        ↓
아이폰 전사문 복사
        ↓
터미널: pbpaste > ~/Downloads/녹취_$(date +%m%d).txt && python3 ~/Desktop/대학원/lecture-notes/scripts/prepare.py
        ↓
Claude.ai에서 노트 생성 → input/ 폴더에 HTML 저장
        ↓
자동: 배치 + 배포 + 알림 🎉
```

---

## ④ 수동 배포 (필요한 경우)

HTML을 `output/[과목]/` 에 직접 넣은 후:

```bash
cd ~/Desktop/대학원/lecture-notes
python3 scripts/deploy.py [과목명] [주차] [날짜(선택)]
```

예시:
```bash
python3 scripts/deploy.py 기독교철학 07 2026.04.16
python3 scripts/deploy.py 기독교철학 07b          # 추가자료
python3 scripts/deploy.py 신약성서I 09            # 오늘 날짜 자동
```

사용 가능한 과목명: `교회사` `기독교철학` `목회학` `신약성서I` `헬라어`

---

## ⑤ 폴더 구조

```
대학원/
  1학기/
    [과목]/
      강의자료/   ← 교수 제공 PPT, PDF (Claude.ai 업로드용)
      녹취/       ← 전사문 .txt (자동 이동됨)
      노트/       ← 생성된 수업정리 HTML (원본명 보관)
      과제/       ← 과제 파일
      _설정/      ← guidelines, 강의계획서

  lecture-notes/
    input/              ← Claude.ai 결과 HTML 저장 위치 👈
      done/             ← 처리 완료된 파일 자동 이동
    output/[과목]/      ← weekNN.html (GitHub Pages 배포본)
    scripts/
      setup.py          ← 최초 설정
      prepare.py        ← STEP 2 실행
      watch.py          ← STEP 1 (감시 앱이 자동 실행)
      deploy.py         ← 수동 배포
      config.json       ← 과목별 URL·경로 설정
    강의노트 감시.app   ← Dock에 추가해서 사용
```

---

## ⑥ 문제 해결

| 증상 | 해결 |
|---|---|
| 녹취 파일이 RTF로 저장됨 | TextEdit → 설정 → 일반 텍스트로 변경 |
| watch.py가 HTML 감지 못함 | `input/` 폴더에 저장했는지 확인 / 감시 앱 실행 중인지 확인 |
| `watchdog 미설치` 오류 | `pip install watchdog` |
| Claude.ai URL 변경 필요 | `python3 scripts/setup.py` 재실행 |
| 배포 실패 | `cd lecture-notes && git status` 로 git 상태 확인 |
