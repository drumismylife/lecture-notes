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

### 4. (선택) NotebookLM 자동 업로드
`setup.py` 실행 중 과목별로 NotebookLM 노트북 ID를 물어봅니다.
- 이미 만든 노트북이 있으면 ID 붙여넣기 (`notebooklm.google.com/notebook/[여기]`)
- 없으면 `n` 입력 → 자동으로 새 노트북 생성
- 그냥 Enter → 비연동(해당 과목은 GitHub Pages 배포만, NotebookLM 업로드 없음)

연동된 과목은 매주 배포 시 STEP 4에서 GitHub Pages URL이 자동으로 NotebookLM 소스로 추가됩니다.

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
- 녹취 파일 → `1학기/[과목]/녹취/` 자동 이동
- Claude Code 요청 문구 안내 출력

---

### STEP 3 | Claude Code에서 노트 생성
prepare.py가 끝나면 안내된 문구를 그대로 이 터미널(Claude Code)에 입력:

```
[과목명] 이번 주 노트 정리해줘
```

`lecture-note-builder` 스킬(`~/.claude/skills/lecture-note-builder/`)이 자동으로:
1. `config.json`에서 과목·프로필(`profile.md`·`syllabus.md`·`theme.json`) 조회
2. `녹취/`·`강의자료/` 폴더에서 해당 주차 파일 읽기
3. 자료근거/교수강조/보충 3출처로 검증·태깅하며 노트 HTML 작성
4. 완성된 HTML을 **아래 폴더에 저장:**

```
~/Desktop/대학원/lecture-notes/input/
```

> Claude.ai 브라우저 업로드 방식(수동)도 여전히 가능합니다 — `setup.py`에서 과목에
> `claude_url`을 등록해두면 그쪽으로도 만들 수 있지만, 기본 경로는 Claude Code입니다.

---

### STEP 4 | 자동 처리 (watch.py가 알아서)
`input/` 폴더에 HTML이 저장되면 자동으로:
1. macOS 팝업 → 과목 선택
2. 주차 입력 (다음 주차 자동 제안, 추가자료면 숫자+b: 예 `10b`)
3. `1학기/[과목]/노트/` 저장 (원본 파일명)
4. `output/[과목]/week10.html` 저장
5. GitHub Pages 자동 배포
5-1. (연동된 과목이면) 배포된 URL을 NotebookLM 소스로 자동 추가
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

사용 가능한 과목명 (2026-08-25 기준, `config.json`의 `subjects`가 원천):
- **1학기(2026-1)**: `교회사` `기독교철학` `목회학` `신약성서I` `헬라어`
- **여름계절(2026-summer)**: `헬라어II` `예배기획`
- **2학기(2026-2, 현재 active)**: `신약성서2` `교회사2` `전도학` `기독교윤리` `예언문학`

> 경로 규칙: `2026-1` 과목만 `output/[과목]/`로 flat 저장(기존 배포 링크 보존). 그 외 모든
> 학기는 `active_semester` 값과 무관하게 항상 `output/<학기ID>/<course_key>/`로 저장된다
> (2026-08-25에 결정론 규칙으로 고정 — 예전엔 active 학기가 바뀔 때마다 경로가 뒤바뀌는
> 버그가 있었음). 새 학기/과목 추가 절차는 `~/Desktop/pgkim-outbox/대학원_강의노트_파이프라인_사용설명서.md` §3 참고.

---

## ⑤ 폴더 구조 (2026-08-25 기준 — 학기별로 동일 패턴 반복)

```
대학원/
  1학기/ · 여름계절/ · 2학기/         ← 학기마다 아래 패턴 반복
    [과목]/
      강의자료/   ← 교수 제공 PPT, PDF (Claude.ai 업로드용)
      녹취/       ← 전사문 .txt (자동 이동됨)
      노트/       ← 생성된 수업정리 HTML (원본명 보관)
      과제/       ← 과제 파일
      _설정/      ← guidelines, 강의계획서(수업계획서 원본)

  lecture-notes/
    input/              ← Claude.ai 결과 HTML 저장 위치 👈
      done/             ← 처리 완료된 파일 자동 이동
    output/
      [과목]/                    ← 1학기 5과목만 flat(레거시 보존, 안 건드림)
      2026-summer/[course_key]/  ← greek2, worship
      2026-2/[course_key]/       ← nt2, hist2, evan, ethic, prophet
    profiles/[course_key]/       ← profile.md·syllabus.md·theme.json (학기 무관, course_key로 고유)
    scripts/
      setup.py          ← 최초 설정
      prepare.py        ← STEP 2 실행
      watch.py          ← STEP 1 (감시 앱이 자동 실행)
      deploy.py         ← 수동 배포 (경로계산은 config.json 기반, §④ 참고)
      update_data.py    ← data.js 편집 로직(deploy.py가 내부 호출)
      config.json       ← 학기·과목별 경로·URL·설정 — 단일 진실원천
    data.js              ← 사이트 전체 데이터(학기·과목·주차·파일 목록)
    강의노트 감시.app   ← Dock에 추가해서 사용
```

> `scripts/pipeline.py`·`scripts/merge.py`·`data/`(마크다운 렌더링 방식)는 2026-08-25에
> 레거시 확정 후 삭제됨 — 현재는 `lecture-note-builder` 스킬이 완성형 HTML을 직접 생성한다.

---

## ⑥ 문제 해결

| 증상 | 해결 |
|---|---|
| 녹취 파일이 RTF로 저장됨 | TextEdit → 설정 → 일반 텍스트로 변경 |
| watch.py가 HTML 감지 못함 | `input/` 폴더에 저장했는지 확인 / 감시 앱 실행 중인지 확인 |
| `watchdog 미설치` 오류 | `pip install watchdog` |
| Claude.ai URL 변경 필요 | `python3 scripts/setup.py` 재실행 |
| 배포 실패 | `cd lecture-notes && git status` 로 git 상태 확인 |
