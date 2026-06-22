// ============================================================
// data.js — M.Div 강의 아카이브 데이터 (학기별 구조)
// 매주 강의노트 생성 후 이 파일만 업데이트하면 됩니다.
//
// 구조: SITE_DATA.semesters[] → 각 학기 { id, label, term, active, courses }
//   courses[과목키] = { meta, syllabus?, tools?, audio?, weeks[], narration? }
//   - meta: 과목 메타데이터 (코드·제목·영문·강조색 acc·설명)
//   - syllabus: 학업계획서 링크 (선택)
//   - tools: 과목 학습 도구/앱 (선택)
//   - audio: 과목 음성 자료 그룹 (선택)
//   - weeks: 주차별 강의 자료
//   각 week.files[] 에 type:'narration' 항목이 있으면 노트 낭독 음성으로 묶임
// ============================================================

const SITE_DATA = {

  semesters: [

    // ════════════════════════════════════════════════════════
    // 2026학년도 1학기
    // ════════════════════════════════════════════════════════
    {
      id: "2026-1",
      label: "2026학년도 1학기",
      term: "2026 Spring",
      active: true,
      courses: {

        greek: {
          meta: {
            code: "LANG 101", title: "헬라어 I", eng: "Koine Greek I", acc: "ag",
            desc: "코이네 그리스어 기초 문법. 알파벳부터 동사 변화까지, 신약 원문 독해를 위한 언어 기반을 다진다.",
            hasApps: true
          },
          tools: [
            {
              name: "헬라어 학습앱1",
              icon: "🔤",
              desc: "알파벳 · 플래시카드 · 퀴즈 · 문법 참고",
              href: "output/greek/night_greek_ver2.html",
              isNew: false
            },
            {
              name: "헬라어 학습앱2",
              icon: "📖",
              desc: "알파벳 발음 · 단어 · 동사변화 오디오 학습",
              href: "https://drumismylife.github.io/greek-study/",
              isNew: false
            },
            {
              name: "중간고사 시험공부 정리",
              icon: "📝",
              desc: "중간고사 대비 시험공부 총정리 학습 페이지",
              href: "output/greek/중간고사_시험공부정리.html",
              isNew: false
            },
            {
              name: "중간고사 퀴즈 앱",
              icon: "🧩",
              desc: "중간고사 대비 문법 퀴즈 — 직접 풀며 점검",
              href: "output/greek/greek-quiz.html",
              isNew: false
            },
            {
              name: "문법 전체 요약 정리",
              icon: "📋",
              desc: "1학기 헬라어 문법 전체 요약 — 기말 과제 제출용",
              href: "output/greek/greek-grammar-summary.html",
              isNew: false
            },
            {
              name: "기말고사 단어 정리 & 퀴즈",
              icon: "🔤",
              desc: "동사·명사·형용사·전치사·대명사 정리 + 3지선다 단어 퀴즈",
              href: "output/greek/greek-vocab.html",
              isNew: false
            },
            {
              name: "기말고사 단어시험 (심화형)",
              icon: "📝",
              desc: "기본형+변화형 4지선다 단어시험, 문제 수 선택 가능",
              href: "output/greek/greek-final-quiz.html",
              isNew: true
            },
            {
              name: "문법노트 PDF (쉬운설명+시험문제)",
              icon: "📕",
              desc: "헬라어 문법 쉬운 설명 + 시험 문제 수록 PDF",
              href: "output/greek/헬라어_문법노트_쉬운설명+시험문제.pdf",
              isNew: false
            },
            {
              name: "단어장 PDF",
              icon: "📗",
              desc: "기말고사 대비 헬라어 단어장 PDF",
              href: "output/greek/TalkFile_헬라어_단어장.pdf.pdf",
              isNew: true
            },
            {
              name: "기말고사 문장 해석",
              icon: "✍️",
              desc: "기말고사 대비 헬라어 문장 해석 연습",
              href: "output/greek/기말고사_문장해석.html",
              isNew: true
            },
            {
              name: "헬라어 기말 총정리",
              icon: "📚",
              desc: "기말고사 대비 핵심 문법·어휘 총정리",
              href: "output/greek/헬라어 기말 총정리.html",
              isNew: true
            }
          ],
          audio: [
            { category: "현재시제", tracks: [
              { name: "현재-수동 1", href: "output/greek/현재-수동1.mp3" },
              { name: "현재-수동 2", href: "output/greek/현재-수동2.mp3" }
            ]},
            { category: "미래시제", tracks: [
              { name: "미래-수동 1", href: "output/greek/미래-수동1.mp3" },
              { name: "미래-수동 2", href: "output/greek/미래-수동2.mp3" }
            ]},
            { category: "단순과거", tracks: [
              { name: "단순과거 능동 직설 1", href: "output/greek/헬라어-단순과거 능동 직설.mp3" },
              { name: "단순과거 능동 직설 2", href: "output/greek/헬라어-단순과거 능동 직설-2.mp3" },
              { name: "단순과거 수동 직설 1", href: "output/greek/헬라어-단순과거 수동 직설.mp3" },
              { name: "단순과거 수동 직설 2", href: "output/greek/헬라어-단순과거 수동 직설-2.mp3" },
              { name: "단순과거 중간 직설 1", href: "output/greek/헬라어-단순과거 중간 직설.mp3" },
              { name: "단순과거 중간 직설 2", href: "output/greek/헬라어-단순과거 중간 직설-2.mp3" }
            ]},
            { category: "미완료", tracks: [
              { name: "미완료 능동 직설 1", href: "output/greek/헬라어-미완료 능동 직설.mp3" },
              { name: "미완료 능동 직설 2", href: "output/greek/헬라어-미완료 능동 직설-2.mp3" },
              { name: "미완료 수동/중간 직설 1", href: "output/greek/헬라어-미완료  수동_중간 직설.mp3" },
              { name: "미완료 수동/중간 직설 2", href: "output/greek/헬라어-미완료  수동_중간 직설-2.mp3" }
            ]}
          ],
          weeks: [
            { week: 1, title: "수업커리큘럼 및 학습 전략", date: "2026.03.09", files: [
                 { type: "notes", label: "강의노트", href: "output/greek/week01.html" }
            ]},
            { week: 2, title: "알파벳 완성 · 이중모음 · 숨표 · 악센트 · 동사 기초", date: "2026.03.16", files: [
              { type: "notes", label: "강의노트", href: "output/greek/week02.html" },
              { type: "pdf", label: "헬라어I_노트정리(홍한나)PDF", href: "output/greek/week02b.pdf" }
            ] },
            { week: 3, title: "현재 능동태 · 수동태 · 중간태 직설법 / 미래 시제 맛보기", date: "2026.03.23", files: [
              { type: "notes", label: "강의노트", href: "output/greek/week03.html" }
            ] },
            { week: 4, title: "복습 & 미래 시제 & 과거 기본", date: "2026.03.30.", files: [
              { type: "notes", label: "강의노트", href: "output/greek/week04.html" },
              { type: "audio", label: "현재수동노래1", href: "output/greek/현재-수동1.mp3" }
            ] },
            { week: 5, title: "교수님 변경 및 복습", date: "2026.04.06.", files: [] },
            { week: 6, title: "시제/태 정리, 전체복습 등", date: "2026.04.13", files: [
              { type: "notes", label: "강의노트", href: "output/greek/week06.html" }
            ] },
            { week: 7, title: "동사의 시제 복습 & 명사(제2변화) 입문", date: "2026.04.20", files: [
                { type: "notes", label: "강의노트", href: "output/greek/week07.html" }
            ] },
            { week: 8, title: "8주차 강의노트", date: "2026.04.27", files: [
                { type: "notes", label: "강의노트", href: "output/greek/week08.html" }
            ] },
            { week: 9, title: "중간고사", date: "2026.05.04", files: [] },
            { week: 10, title: "어휘 · 명사 · 관사 · 관계대명사 · 형용사", date: "2026.05.11", files: [
                { type: "notes", label: "강의노트", href: "output/greek/week10.html" }
            ] },
            { week: 11, title: "형용사와 인칭대명사", date: "2026.05.18", files: [
                { type: "notes", label: "강의노트", href: "output/greek/week11.html" }
            ] },
            { week: 12, title: "형용사 · 인칭대명사 복습 + εἰμί 동사 · 지시대명사", date: "2026.05.25", files: [
                { type: "notes", label: "강의노트", href: "output/greek/week12.html" }
            ] },
            { week: 13, title: "부정사와 종속절", date: "2026.06", files: [] },
            { week: 14, title: "신약 본문 독해 실습", date: "2026.06", files: [] },
            { week: 15, title: "기말고사", date: "2026.06", files: [] },
          ]
        },

        min: {
          meta: {
            code: "MIN 201", title: "목회학", eng: "Pastoral Ministry", acc: "am",
            desc: "목회자의 정체성과 소명, 설교·예배·심방·상담의 실천 신학적 기초를 다룬다."
          },
          weeks: [
            { week: 1, title: "오리엔테이션 & 목회의 개념", date: "2026.03.09.", files: [
              { type: "notes", label: "강의노트", href: "output/목회학/week01.html" }
            ] },
            { week: 2, title: "목회란 무엇인가", date: "2026.03.16.", files: [
              { type: "notes", label: "강의노트", href: "output/목회학/week02.html" }
            ] },
            { week: 3, title: "목회와 목회자", date: "2026.03.23.", files: [
              { type: "notes", label: "강의노트", href: "output/목회학/week03.html" }
            ] },
            { week: 4, title: "목회자의 소명 & 목회와 목회자(2)", date: "2026.03.30", files: [
              { type: "notes", label: "강의노트", href: "output/목회학/week04.html" }
            ] },
            { week: 5, title: "목회자의 정체성과 자기 관리", date: "2026.4.6.", files: [
              { type: "notes", label: "강의노트", href: "output/목회학/week05.html" }
            ] },
            { week: 6, title: "목회자의 영성 관리", date: "2026.04.13.", files: [
              { type: "notes", label: "강의노트", href: "output/목회학/week06.html" }
            ] },
            { week: 7, title: "목회와 설교 & 목회자의 준비", date: "2026.04.20", files: [
                { type: "notes", label: "강의노트", href: "output/목회학/week07.html" }
            ] },
            { week: 8, title: "중간고사", date: "2026.05", files: [
                { type: "notes", label: "강의노트", href: "output/greek/week08.html" }
            ] },
            { week: 9, title: "목회 리더십 — 권력과 권위, 서번트 리더십", date: "2026.05.04", files: [
                { type: "notes", label: "강의노트", href: "output/목회학/week09.html" }
            ] },
            { week: 10, title: "현대인의 종교 성향 변화와 교회의 대응", date: "2026.05.11", files: [
                { type: "notes", label: "강의노트", href: "output/목회학/week10.html" }
            ] },
            { week: 11, title: "현대 목회와 예배", date: "2026.05.18", files: [
                { type: "notes", label: "강의노트", href: "output/목회학/week11.html" }
            ] },
            { week: 12, title: "목회와 교육 · 목회와 설교", date: "2026.05.25", files: [
                { type: "notes", label: "강의노트", href: "output/목회학/week12.html" }
            ] },
            { week: 13, title: "어떻게 목회할 것인가?", date: "2026.06.01", files: [
                { type: "notes", label: "강의노트", href: "output/목회학/week13.html" }
            ] },
            { week: 14, title: "목회와 소그룹", date: "2026.06.08", files: [
                { type: "notes", label: "강의노트", href: "output/목회학/week14.html" }
            ] },
            { week: 15, title: "건강한 교회를 세우기 위한 목회 방법", date: "2026.06.15", files: [
                { type: "notes", label: "강의노트", href: "output/목회학/week15.html" }
            ] },
          ]
        },

        phil: {
          meta: {
            code: "PHIL 301", title: "기독교철학", eng: "Christian Philosophy", acc: "ap",
            desc: "Friedo Ricken의 Religionsphilosophie를 중심으로 종교철학의 핵심 논제를 탐구한다."
          },
          weeks: [
            { week: 1, title: "기독교철학의 학습가이드", date: "2026.03.03.", files: [
                { type: "notes", label: "강의노트", href: "output/기독교철학/week01.html" }
            ] },
            { week: 2, title: "종교란 무엇인가", date: "2026.03.10.", files: [
                { type: "notes", label: "강의노트", href: "output/기독교철학/week02.html" }
            ] },
            { week: 3, title: "비트겐슈타인 신앙의 경험과 언어의 의미 & 사유에 한계를 짓기", date: "2026.03.17.", files: [
                { type: "notes", label: "강의노트1", href: "output/기독교철학/week03.html" },
                { type: "notes", label: "강의노트2", href: "output/기독교철학/week03b.html" }
            ] },
            { week: 4, title: "비트겐슈타인 문화적 가치와 철학|종교적 근본행위 · 윌리엄 제임스", date: "2026.03.24", files: [
                { type: "notes", label: "강의노트", href: "output/기독교철학/week04.html" },
                { type: "notes", label: "강의노트_업그레이드", href: "output/기독교철학/week04b.html" },
                { type: "audio", label: "음성노트정리", href: "output/기독교철학/음성강의정리.m4a" }
            ] },
            { week: 5, title: "윌리엄 제임스", date: "2026.03.31", files: [
                 { type: "notes", label: "강의노트", href: "output/기독교철학/week05.html" },
                 { type: "notes", label: "강의노트(업데이트)", href: "output/기독교철학/week05b.html" }
            ] },
            { week: 6, title: "레비나스 — 계시의 개념과 메시아적 종교", date: "2026.04.07", files: [
                 { type: "notes", label: "강의노트", href: "output/기독교철학/week06.html" },
                 { type: "notes", label: "강의노트(업데이트)", href: "output/기독교철학/week06b.html" }
            ] },
            { week: 7, title: "찰스 샌더스 퍼스", date: "2026.04.14", files: [
                { type: "notes", label: "강의노트", href: "output/기독교철학/week07.html" }
            ] },
            { week: 8, title: "중간고사", date: "2026.05", files: [] },
            { week: 9, title: "존 헨리 뉴먼", date: "2026.04.29", files: [
                { type: "notes", label: "강의노트", href: "output/기독교철학/week09.html" }
            ] },
            { week: 10, title: "템플 그랜딘을 통해 사유하기", date: "2026.05.05", files: [
                { type: "notes", label: "강의노트", href: "output/기독교철학/week10.html" }
            ] },
            { week: 11, title: "임마누엘 칸트", date: "2026.05.12", files: [
                { type: "notes", label: "강의노트", href: "output/기독교철학/week11.html" },
                { type: "notes", label: "임마누엘 칸트", href: "output/기독교철학/week11b.html" }
            ] },
            { week: 12, title: "폴 리쾨르 — 실재에 관한 탐구로서의 철학과 신학", date: "2026.05.19", files: [
                { type: "notes", label: "강의노트", href: "output/기독교철학/week12.html" },
                { type: "notes", label: "폴 리쾨르 — 해석학과 신학적 자기 이해", href: "output/기독교철학/week12b.html" }
            ] },
            { week: 13, title: "슐라이어마허 — 종교의 장애와 본질에 대하여", date: "2026.05.26", files: [
                { type: "notes", label: "강의노트", href: "output/기독교철학/week13.html" }
            ] },
            { week: 14, title: "기독교 윤리의 철학적 기초", date: "2026.06", files: [] },
            { week: 15, title: "기말고사", date: "2026.06", files: [] },
          ]
        },

        nt: {
          meta: {
            code: "NT 401", title: "신약성서 I", eng: "New Testament I", acc: "an",
            desc: "공관복음 개론, 마태복음의 신학적 구조와 기독론, 편집비평적 관점에서의 분석."
          },
          audio: [
            { category: "누가복음-사도행전 요약", tracks: [
              { name: "누가복음-사도행전 요약 1", href: "output/신약성서I/누가복음-사도행전 요약ver1.m4a" },
              { name: "누가복음-사도행전 요약 2", href: "output/신약성서I/누가복음-사도행전 요약ver2.m4a" }
            ]}
          ],
          weeks: [
            { week: 1, title: "신구약 중간기 & 수전절", date: "2026.03.05.", files: [
                { type: "notes", label: "강의노트", href: "output/신약성서I/week01.html" }
            ] },
            { week: 2, title: "마태복음 개론 + 신약성서의 세계", date: "2026.03.12.", files: [
                { type: "notes", label: "강의노트", href: "output/신약성서I/week02.html" }
            ] },
            { week: 3, title: "신약성서의 세계와 신약의 문헌들", date: "2026.03.19.", files: [
                { type: "notes", label: "강의노트", href: "output/신약성서I/week03.html" }
            ] },
            { week: 4, title: "신약 27권 구조 · 정경 · 본문비평 · 석의", date: "2026.03.26.", files: [
                { type: "notes", label: "강의노트", href: "output/신약성서I/week04.html" }
            ] },
            { week: 5, title: "마가복음 — 고난받는 종의 복음서", date: "2026.04.02.", files: [
                { type: "notes", label: "강의노트", href: "output/신약성서I/week05.html" }
            ] },
            { week: 6, title: "사회인류학의 도움을 받아 신약성서 이해하기", date: "2026.04.09", files: [
              { type: "notes", label: "강의노트", href: "output/신약성서I/week06.html" },
              { type: "notes", label: "중간고사 문제 안내 & 준비 가이드", href: "output/신약성서I/week06b.html" }
            ] },
            { week: 7, title: "마가복음 남은 이야기 + 누가복음 도입", date: "2026.04", files: [
                { type: "notes", label: "강의노트", href: "output/신약성서I/week07.html" }
            ] },
            { week: 8, title: "중간고사", date: "2026.05", files: [] },
            { week: 9, title: "누가복음 전체 정리", date: "2026.04.30", files: [
                { type: "notes", label: "강의노트", href: "output/신약성서I/week09.html" }
            ] },
            { week: 10, title: "누가복음 마지막 이야기", date: "2026.05.07", files: [
                { type: "notes", label: "강의노트", href: "output/신약성서I/week10.html" }
            ] },
            { week: 11, title: "요한복음 — 첫 이야기", date: "2026.05.14", files: [
                { type: "notes", label: "강의노트", href: "output/신약성서I/week11.html" }
            ] },
            { week: 12, title: "12주차 요한복음 두 번째 이야기", date: "2026.05.21", files: [
                { type: "notes", label: "강의노트", href: "output/신약성서I/week12.html" }
            ] },
            { week: 13, title: "사도행전 첫 번째 이야기", date: "2026.05.28", files: [
                { type: "notes", label: "강의노트", href: "output/신약성서I/week13.html" }
            ] },
            { week: 14, title: "사도행전 두 번째(마지막) 이야기", date: "2026.06.04", files: [
                { type: "notes", label: "강의노트", href: "output/신약성서I/week14.html" }
            ] },
            { week: 15, title: "기말고사", date: "2026.06", files: [] },
          ]
        },

        hist: {
          meta: {
            code: "HIST 201", title: "교회사개론 I", eng: "Church History I", acc: "ah",
            desc: "초대교회부터 종교개혁까지, 기독교 역사의 흐름과 신학적 사건들을 개괄한다."
          },
          weeks: [
            { week: 1, title: "기독교 교회사 입문", date: "2026.03.06", files: [
                { type: "notes", label: "강의노트", href: "output/교회사/week01.html" }
            ] },
            { week: 2, title: "기독교 형성과 사도시대 I 예수와 유대교의 연관성·분파", date: "2026.03.13", files: [
              { type: "notes", label: "강의노트", href: "output/교회사/week02.html" }
            ] },
            { week: 3, title: "기독교 형성과 사도시대 II", date: "2026.03.20", files: [
                { type: "notes", label: "강의노트1", href: "output/교회사/week03.html" },
                { type: "notes", label: "강의노트2", href: "output/교회사/week03b.html" }
            ] },
            { week: 4, title: "예루살렘과 그 너머 & 사도 바울", date: "2026.03.27", files: [
               { type: "notes", label: "강의노트", href: "output/교회사/week04.html" }
            ] },
            { week: 5, title: "바울 이후 기독교 — 지리적 확장·선교·핍박과 변증", date: "2026.4.3", files: [
               { type: "notes", label: "강의노트", href: "output/교회사/week05.html" }
            ] },
            { week: 6, title: "8장 함께 사는 삶", date: "2026.04", files: [
               { type: "notes", label: "강의노트", href: "output/교회사/week06.html" }
            ] },
            { week: 7, title: "교회사개론 I — Historia Ecclesiae", date: "2026.04.17", files: [
                { type: "notes", label: "강의노트", href: "output/교회사/week07.html" }
            ] },
            { week: 8, title: "이슬람교에 대한 이해", date: "2026.04.24", files: [
                { type: "notes", label: "강의노트", href: "output/교회사/week08.html" }
            ] },
            { week: 9, title: "제3부 새로운 상황 (AD 175–313)", date: "2026.05.01", files: [
                { type: "notes", label: "강의노트", href: "output/교회사/week09.html" }
            ] },
            { week: 10, title: "기독교 로마제국시대 II", date: "2026.05.08", files: [
                { type: "notes", label: "강의노트", href: "output/교회사/week10.html" }
            ] },
            { week: 11, title: "11주차: 기독론 공의회 · 수도원 운동 · 어거스틴", date: "2026.05.15", files: [
                { type: "notes", label: "강의노트", href: "output/교회사/week11.html" }
            ] },
            { week: 12, title: "어거스틴 심화 · 교황제도 · 동서 교회 분열", date: "2026.05.22", files: [
                { type: "notes", label: "강의노트", href: "output/교회사/week12.html" }
            ] },
            { week: 13, title: "중세 기독교 시대 I", date: "2026.05.29", files: [
                { type: "notes", label: "강의노트", href: "output/교회사/week13.html" }
            ] },
            { week: 14, title: "14주차: 중세기독교 시대 II", date: "2026.06.05", files: [
                { type: "notes", label: "강의노트", href: "output/교회사/week14.html" }
            ] },
            { week: 15, title: "기말고사", date: "2026.06", files: [] },
          ]
        }

      }
    },

    // ════════════════════════════════════════════════════════
    // 2026학년도 여름 계절학기 (구조만 — 과목 확정 시 채움, 보통 2과목)
    // ════════════════════════════════════════════════════════
    {
      id: "2026-summer",
      label: "2026학년도 여름 계절학기",
      term: "2026 Summer",
      active: false,
      courses: {

        greek2: {
          meta: {
            code: "LANG 102", title: "헬라어 II", eng: "Koine Greek II", acc: "ag",
            desc: "코이네 그리스어 중급(안호준·장석조 교재) — 동사상(verbal aspect) 중심으로 부정과거·완료·분사·명령법 등 동사 체계를 확장하고 신약 본문 해석에 적용한다.",
            hasApps: true
          },
          syllabus: { href: "output/2026-summer/greek2/syllabus.html", type: "syllabus" },
          tools: [
            {
              name: "1학기 총정리 → 헬라어 II 준비",
              icon: "🌉",
              desc: "1학기 전체 패러다임 복습 + 2학기 예습 브릿지 (메이첸 기준)",
              href: "output/2026-summer/greek2/greek-bridge-1to2.html",
              isNew: true
            }
          ],
          weeks: [
            { week: 1, title: "오리엔테이션 + 복습1 — 알파벳·억양·음절, 동사(1-1) 현재 능동, 명사 2변화·관사, 명사 1변화", date: "2026.06.29", files: [] },
            { week: 2, title: "복습2 — 형용사 1·2변화, 전치사·인칭대명사, 동사(1-2) 현재 중·수동, 동사(2) 미완료, 부사(1), 명사 3변화·부정어", date: "2026.06.29", files: [] },
            { week: 3, title: "동사(3-1) 직설법 부정과거 능동·중간", date: "2026.06.30", files: [] },
            { week: 4, title: "동사(3-2) 부정과거 수동 · 수사 · 부사(2)", date: "2026.06.30", files: [] },
            { week: 5, title: "단축동사(직설법) · 지시대명사", date: "2026.07.02", files: [] },
            { week: 6, title: "유음동사(직설법) · 재귀대명사", date: "2026.07.02", files: [] },
            { week: 7, title: "동사(4) 직설법 미래시제", date: "2026.07.03", files: [] },
            { week: 8, title: "중간고사 (11–15과, 본문 해석 위주)", date: "2026.07.03", files: [] },
            { week: 9, title: "동사(5) 직설법 현재완료·과거완료", date: "2026.07.06", files: [] },
            { week: 10, title: "분사(1) 현재시제", date: "2026.07.06", files: [] },
            { week: 11, title: "분사(2) 부정과거시제", date: "2026.07.07", files: [] },
            { week: 12, title: "분사(3) 완료·미래시제", date: "2026.07.07", files: [] },
            { week: 13, title: "명령법", date: "2026.07.09", files: [] },
            { week: 14, title: "남은 문법 정리 — 접속사·관계대명사, 가정법, 형용사(2)·부사(3), 부정사(법)", date: "2026.07.09", files: [] },
            { week: 15, title: "기말고사 (16–20과, 본문 해석 위주)", date: "2026.07.10", files: [] },
          ]
        },

        worship: {
          meta: {
            code: "WOR 61087", title: "예배기획", eng: "Worship Design", acc: "ap",
            desc: "예배의 성경적·신학적 기초 위에 예배 구조·교회력·음악·멀티미디어를 이해하고, 각 교회 현실에 맞는 예배 기획안을 작성하는 이론+적용 과목(김은영, 온라인)."
          },
          syllabus: { href: "output/2026-summer/worship/syllabus.html", type: "syllabus" },
          weeks: [
            { week: 1, title: "수업 개요 · 수업 소개", date: "", files: [] },
            { week: 2, title: "예배 기획의 신학적 기초 및 역사 — 예배 정의·성경 속 예배 모델·예배 발전과 역사", date: "", files: [] },
            { week: 3, title: "예배의 구조와 요소 — 구조 이해·각 순서 이해·나의 교회 예배 구조 분석", date: "", files: [] },
            { week: 4, title: "예배와 음악 — 순서에 따른 선곡·회중 찬양 이해", date: "", files: [] },
            { week: 5, title: "교회력의 이해와 예배 기획 — 교회력·선곡·절기 예배 기획", date: "", files: [] },
            { week: 6, title: "예배기획 과제 실습 — 영상 통한 예배 분석·종려주일 예배 사례 분석", date: "", files: [] },
            { week: 7, title: "예배 형식과 악기의 이해 — 예배 악기·악기 활용·음향/영상/자막", date: "", files: [] },
            { week: 8, title: "중간고사 — 교회력 절기 예배 기획안 제출", date: "2026.07.05", files: [] },
            { week: 9, title: "침례교 예배와 특별 예배 기획 — 정체성·목적에 따른 특별 예배", date: "", files: [] },
            { week: 10, title: "열린예배와 한국교회 — 예배학적 관점·영상 분석", date: "", files: [] },
            { week: 11, title: "세대통합예배 — 모든 세대가 함께 드리는 예배", date: "", files: [] },
            { week: 12, title: "블렌디드 워십 — 이해와 예배 사역 적용", date: "", files: [] },
            { week: 13, title: "예배 기획을 위한 사례 연구 — 다양한 예배 관찰·분석", date: "", files: [] },
            { week: 14, title: "중간고사 리뷰 — 우수 기획안 3–4개 공유·분석", date: "", files: [] },
            { week: 15, title: "기말고사 — 주일 예배 기획안 제출", date: "2026.07.10", files: [] },
          ]
        }

      }
    },

    // ════════════════════════════════════════════════════════
    // 2026학년도 2학기 (구조만 — 과목 확정 시 채움)
    // ════════════════════════════════════════════════════════
    {
      id: "2026-2",
      label: "2026학년도 2학기",
      term: "2026 Fall",
      active: false,
      courses: {}
    }

  ],

  // ── 관련 자료 (전역) ────────────────────────────────────────
  resources: [
    {
      label: "헬라어 학습",
      items: [
        {
          icon: "📘", name: "Bible Hub — 원어 사전",
          desc: "Strong's 번호 기반 헬라어·히브리어 사전",
          href: "https://biblehub.com/lexicon/",
          tag: "greek", tagLabel: "헬라어"
        },
        {
          icon: "📗", name: "Blue Letter Bible",
          desc: "원문 대조, 주석, 어휘 분석 통합 플랫폼",
          href: "https://www.blueletterbible.org",
          tag: "greek", tagLabel: "헬라어"
        },
      ]
    },
    {
      label: "성경 & 신학",
      items: [
        {
          icon: "📖", name: "대한성서공회 성경",
          desc: "개역개정 · 새번역 온라인 열람",
          href: "https://www.bskorea.or.kr",
          tag: "bible", tagLabel: "성경"
        },
        {
          icon: "🏛️", name: "한국침례신학대학교",
          desc: "학교 공식 홈페이지",
          href: "https://www.kbtus.ac.kr",
          tag: "gen", tagLabel: "학교"
        },
      ]
    }
  ]
};
