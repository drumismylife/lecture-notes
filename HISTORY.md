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

## 2026-09-01~02 — 2학기 착수: 예언문학 1·2주차 + Panopto 자막 자동추출 + sermon 스킬 교차검증

**2학기 첫 실착수**. 예언문학(오성호 교수, 100% Panopto 온라인 강의)의 1주차(소선지서
서론)·2주차(호세아서)를 `output/2026-2/prophet/week01.html`·`week02.html`로 생성·배포
완료(둘 다 각 2개 영상, PPT 없이 자막만 근거). `config.json`의 예언문학·기독교윤리 두
과목에 `"video_source": "panopto"` 필드 신설(헬라어II 여름계절 선례와 동일 패턴) — 두
과목 다 담당교수가 "전 주차 영상강의"로 profile.md에 이미 명시돼 있었음.

**Panopto 자막 자동추출 기법 확립(수동 콘솔 스크립트 불필요)**: 기존 SKILL.md는 "사용자가
Safari 콘솔에서 `PanoptoViewer.Services.getCaptions()` 실행 후 붙여넣기"만 안내했는데,
이번에 완전 자동화 경로를 발견:
1. Safari 설정에서 "Apple 이벤트로부터 JavaScript 허용"(Develop 메뉴)을 오너가 1회
   켜면, `osascript`의 `do JavaScript ... in document` 로 세션이 직접 페이지에 JS를
   실행할 수 있게 됨(이미 로그인된 실제 브라우저 쿠키 그대로 사용 — 별도 로그인 자동화
   불필요, 2026-08-18 "제미나이 웹 로그인 자동화 차단됨" 사례와 무관한 정상 경로).
2. LMS 강의창(`edulms.kbtus.ac.kr`)은 실제 Panopto 플레이어를 **같은 출처의 중첩
   iframe**(`doViewLectureWindow.dunet`) 안에 다시 cross-origin iframe(`panopto.com/
   .../Embed.aspx?id=...`)으로 얹어놓는 구조 — 바깥 프레임이 LMS와 동일 출처이므로
   `document.querySelector("iframe").contentDocument.querySelectorAll("iframe")` 로
   중첩 iframe의 `src`(진짜 Panopto 세션 UUID 포함)를 그대로 읽어낼 수 있음.
3. 그 세션 ID로 `GenerateSRT.ashx?id=<uuid>&language=Korean` 를 fetch하면 SRT 전문이
   바로 반환됨(Panopto 세션 검색 API `/Panopto/api/v1/sessions/search`도 보조로 유용하나
   최근 업로드는 인덱싱 지연이 있어 신뢰 못함 — LMS iframe 경로가 더 확실함).
4. 오너는 그냥 LMS에서 원하는 강의를 클릭해 열어주기만 하면 됨(자막 켜기·콘솔 조작 불요).
이 절차는 `SKILL.md`에는 아직 반영 안 함(오성호 교수 강의는 이 학교 LMS 특유 구조라 다른
학교/과목에서 재현 안 될 수 있음 — 재현 시 SKILL.md의 "(b) Panopto" 절 갱신 검토).

**용어 2차 교차검증 체계 신설**: 예언문학·신약성서처럼 PPT 없이 자막만으로 노트를 만드는
과목은 인명·원어·역사배경의 ASR 오인식이 특히 잦다는 오너 지적으로, `~/.claude/skills/
lecture-note-builder/SKILL.md`에 "용어 2차 교차검증 — related_skills 활용" 절 신설.
`config.json`의 과목별 `related_skills`(sermon-bible-dictionary 등)가 다루는 영역
(성경 인물·지명·원어·역사문화배경)과 다루지 않는 영역(현대 학자 2차문헌 인명)을 명확히
구분해, 후자는 별도 웹검색으로 보강하되 특정 못하면 가짜 확정 없이 "특정 불가"로 남기게
함. 2주차 노트의 ASR 불확실 학자명 5명(텐샴→F. Charles Fensham, 크리스텐센→Duane L.
Christensen, 콜린스→Terence Collins, 그리스만→Hugo Gressmann, 영가→E. J. Young 추정)
조사를 cys 워커(제미나이)에 위임 → 결과를 마스터가 직접 재검증(실존 확인은 됐으나 원문
문장 1:1 대조까지는 안 된 항목은 "유력·확정 아님"으로 정직하게 표기, 워커 완료보고를
곧이곧대로 신뢰하지 않는 원칙 그대로 적용)한 뒤 두 노트에 반영·재배포.

**"책별 참고서" 시리즈 신설(같은 날 이어서)**: 오너가 "주차 노트를 뛰어넘는, 수업계획서
지정 참고도서 내용까지 최대한 확보한 성경책별 참고서"를 요청 — 단, 그 참고도서(김창대·
매콤빌·롱맨/딜라드·반게메렌·치솜·하우스)의 실제 원문은 이 세션이 열람할 수 없어, 오너가
"학술지식과 웹검색으로 검증된·신학적으로 온전한 자료를 만들어달라"고 방법론을 확정해줌
(참고도서 내용은 "이렇게 알려져 있다"는 정직한 프레이밍, 원문 인용처럼 단정 금지). 예언문학
·신약성서 과목 전체에 걸쳐 **책마다** 만들어가는 시리즈로 확정 — 오늘은 그 1편으로
`output/2026-2/prophet/guide_hosea.html`(호세아서 참고서: 시대배경 심화·문학구조 학계
정리·핵심 원어 5개·본문 강해 8곳·신약 인용 4곳·참고도서 6권 소개·묵상질문) 제작 —
`add_back_button.py`는 `deploy.py`가 다루는 "주차" 개념 밖이라 수동 실행.

**배치 위치 정정(같은 날, 오너 피드백)**: 처음엔 `data.js`의 `prophet.tools[]`(과목 상단
전역 도구 영역)에 등록했으나, 오너가 "강의계획서상 한 주차=한 선지서 구조이니 참고서도 해당
주차 강의노트 옆이 낫겠다"고 정정 — `tools[]`에서 빼고 **week2.files[]**에 `type: "guide"`
항목으로 이동(`index.html`의 `FMETA`에 `guide:{icon:'📚',label:'참고서',chip:'chip-notes'}`
신설, `week.files`는 `FMETA[f.type]||FMETA.other` 폴백이 있어 새 타입 추가가 안전함을 확인
후 적용). **최종 확정 절차**: 앞으로 책별 참고서는 `weekNN.files[]`에 `guide` 타입으로
해당 주차 강의노트와 나란히 등록한다(과목 tools가 아님) — 요엘·아모스 등 다음 책부터
이 절차를 기본으로 따를 것.

**"안 바뀌었어" 버그 — index.html의 data.js 캐시버전 고정 발견·수정**: 위 정정을 배포했는데도
오너 브라우저에 반영이 안 됨 — 원인은 `index.html`의 `<script src="data.js?v=20260615h">`가
이 세션의 여러 `data.js` 수정(예언문학 1·2주차, 호세아서 참고서 등)에도 **한 번도 안 바뀌어**
방문자 브라우저가 옛 캐시를 계속 재사용하고 있었던 것(GitHub Pages 자체는 최신 파일 서빙 중 —
`curl`로는 항상 최신이 보여 이 세션도 한동안 못 알아챔). `git log`로 확인한 기존 버전 문자열
관행(`YYYYMMDD[a-z]` — 같은 날 여러 번 갱신 시 알파벳 접미사 증가)에 맞춰
`scripts/update_data.py`에 `bump_index_cache_version()` 신설, `update()` 끝에서 자동 호출하도록
연결 — **`deploy.py` 정상 경로에서는 앞으로 자동 재발방지**. 단, `update()`는 `files: []`가
비어있는 최초 등록 때만 동작하므로(이미 채워진 주차를 수동 편집하는 경우엔 트리거 안 됨) 이번
같은 수동 `data.js` 편집 후에는 여전히 `bump_index_cache_version()`을 손으로 한 번 불러줘야
한다 — 앞으로 수동 편집 시 잊지 말 것.
