# 강의노트 파이프라인 이력

장기메모리에서 이관(2026-08-27 메모리 정리). 시스템 사용법은 `README.md`, 스킬 사용법은
`~/.claude/skills/lecture-note-builder/SKILL.md` 참조 — 이 문서는 "왜 지금 이 형태가
됐는가"만 다룬다.

## 배경

오너(김평강, 한침대 M.Div 대학원생)가 `~/Desktop/대학원/lecture-notes/`에서 운영 중
(git repo, GitHub Pages 배포: `drumismylife.github.io/lecture-notes`). 1학기(기독교철학·
교회사·목회학·신약성서I·헬라어)·여름계절학기(헬라어II·예배기획) 완료.

**시스템 구조**: `scripts/prepare.py` → `watch.py`(input/ 감시, macOS 다이얼로그로 과목·
주차 확인) → `scripts/deploy.py`(data.js 갱신 + git push + NotebookLM 업로드).
`profiles/<course_key>/`에 과목별 `profile.md`(노트 구조·강조점)·`syllabus.md`(학업계획서)·
`theme.json`(디자인 토큰). `~/.claude/skills/lecture-note-builder/SKILL.md`가 실제 노트
생성을 담당(할루시네이션0, 4출처 태깅: 자료근거/교수강조/강의추가/보충).

## 2026-07-16 — Claude.ai에서 Claude Code로 전환

1학기 방식(매주 Claude.ai 웹에 수동 업로드)은 이미 profile.md/syllabus.md 파일로 같은
맥락을 미러링해두고 있어서, Claude Code 쪽이 완전 자동화(브라우저 왕복 제거)에 유리하다고
판단해 오너가 전환 결정. 변경 내용(당시 미커밋, 2학기 확정 때 같이 커밋 예정이었음 —
`git status`로 커밋 여부 재확인할 것):
1. `deploy.py`에 NotebookLM 자동 소스 추가 단계 — `config.json` 과목에 `notebook_id`가
   있으면 배포된 GitHub Pages URL을 `nlm source add`로 자동 추가.
2. `setup.py`에 NotebookLM 노트북 연결 단계(기존 ID 입력 또는 즉석 생성).
3. `prepare.py`의 Claude.ai 브라우저 자동 오픈 제거 → "Claude Code에게 요청하세요" 안내로
   대체.
4. `README.md` STEP 3을 Claude Code 기반으로 재작성(Claude.ai 수동 방식은 옵션으로 유지).

**용어 참고**: "NotebookLM"은 2026-07-16부로 "Gemini Notebook"으로 개명됨(같은 제품, `nlm`
CLI 그대로 작동 — 마이그레이션 불필요). 오너가 "제미나이 노트북"이라 하면 동일 대상.

## 2026-08-03 — GitHub 인증 전환

이 레포의 git push 인증을 classic PAT(macOS 키체인 경유)에서 `gh` CLI OAuth 기반으로 전환
(`gh auth setup-git` 실행, github.com 전용 credential.helper를 `gh auth git-credential`로
설정). 계기: 그 PAT가 "7일 후 만료" 메일을 보내 매번 수동 재발급하는 대신 근본 해결을
선택. 이후 classic PAT는 미사용(만료돼도 영향 없음). 이 레포·다른 github.com 레포에서
"토큰 만료" 알림이 다시 오면 먼저 `gh auth status`로 현재 인증 방식부터 확인할 것.

## 2026-08-04 — 노트 품질 검증 로직 강화

오너가 실제 녹취 예제(31,218자, 줄바꿈 0개 통짜 텍스트, 동일 인물명이 4가지로 다르게
표기됨)를 보여주며 "녹취 해석 정확도"를 1순위 문제로 지적 — `SKILL.md`와 5개 profile.md
(greek/nt/hist/phil/min)를 수정:

1. **3출처 → 4출처**: 자료근거/교수강조/보충에 **"강의추가"**(PPT엔 없고 녹취에만 있는
   내용) 신설.
2. **세그먼트 원장**: 녹취 전체를 화제전환 신호 기준으로 나눠 처리여부를 표로 추적 —
   HTML 작성 전 100% 채워야 다음 단계 진행 가능(긴 스크립트 뒷부분 누락 방지용 구조적
   장치).
3. **ASR 오인식 보정 전면화**: 기존엔 원어·표·수식(주로 헬라어)에만 있던 규칙을 전 입력
   모드로 확대. 핵심 원칙 — 어색한 구간을 매끄럽게 "고쳐 쓰지 않고" 원문 보존 +
   `[ASR 불확실: "..."]` 표시. 임의 보정은 할루시네이션과 동일 취급.
4. **PPT↔녹취 3자 대조**: "자료근거"로 뭉뚱그리던 것을 PPT+녹취 공통 / 녹취전용(강의추가) /
   PPT엔 있으나 녹취 미언급(검증요약에 별도 리스트)으로 분리.
5. **잡담↔예화 구분**: 순수 사담은 배제하되 교훈적 일화는 보존 — 특히 `min`(목회학)은
   노트구조 자체에 "사례/예화" 섹션이 있어 profile.md에 별도 강조.
6. 각 profile.md에 `## 검증 강도` 섹션 신설 — 과목별 ASR 엄격도·PPT 의존도 차등화
   (헬라어/교회사=최고강도, 신약/철학=높음, 목회학=보통+예화 특이사항).

**같은 날 — greek2·worship profile.md 2학기 사전 검토**: 두 과목 다 `## 검증 강도` 섹션이
빠져있어 신설(greek2=최고강도+자료의존도 높음/교재캡처 1차자료, worship=보통+PPT의존도
낮음/온라인강의라 "강의추가" 잦음).

**데이터 유실 직전 상황 발견·복구**: greek2/profile.md가 "원어 정확도의 기준 원본"으로
지정한 `교재전체캡처본`(1.3G)·`연습문제캡처본`(211M)이 같은 날 폴더정리 직후 오너의
"그 파일들 그냥 지웠어" 발언 대상이었던 것으로 확인 — 실제로는 완전삭제가 아니라
`~/Library/Mobile Documents/.Trash/`(iCloud 자체 휴지통)에 있었음. `ditto`(일반 `mv`는
여기서도 mmap과 같은 "Resource deadlock avoided"로 실패 — iCloud 휴지통 경계를 넘는
이동 자체가 이 오류를 유발하는 듯)로 새 위치(`~/Desktop/대학원/여름계절/헬라어II/강의자료/`)
로 복구 완료, 파일수·용량 일치 확인. profile.md의 경로 참조도 새 위치로 수정. 원본은
iCloud 휴지통에 그대로 둠(자동 만료 대기, 위험 없음).

## 커밋 방침 (2026-08-04 시점 기록)

`profile.md` 5개는 git 추적 대상이라 수정됐지만, 오너가 "2학기 확정 때 같이 묶어서
커밋"하기로 함 — 07-16 미커밋 변경(deploy.py/setup.py/prepare.py/README.md)과 합쳐서
한 번에 커밋 예정. `SKILL.md`는 `~/.claude/skills/` 소속이라 이 레포 git 추적 대상이
아님(커밋 이슈 없음). 2학기 과목 확정 요청이 오면 이 배경 그대로 활용해 한 번에 커밋
안내(단, 이후 세션에서 실제로 커밋됐는지는 `git log`로 재확인할 것 — 이 문서는
2026-08-04 시점 스냅샷).
