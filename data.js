// ============================================================
// data.js — M.Div 강의 아카이브 데이터
// 매주 강의노트 생성 후 이 파일만 업데이트하면 됩니다.
// ============================================================

const SITE_DATA = {

  // ── 과목별 주차 데이터 ──────────────────────────────────────
  courses: {

    greek: {
      weeks: [
        {
          week: 1,
          title: "수업커리큘럼 및 학습 전략",
          date: "2026.03.09",
          files: [
             { type: "notes", label: "강의노트", href: "output/greek/week01.html" }
          ]
        },
        { week: 2, title: "알파벳 완성 · 이중모음 · 숨표 · 악센트 · 동사 기초", date: "2026.03.16", files: [
          { type: "notes", label: "강의노트", href: "output/greek/week02.html" }
        ] },
        { week: 3, title: "현재 능동태 · 수동태 · 중간태 직설법 / 미래 시제 맛보기", date: "2026.03.23", files: [
          { type: "notes", label: "강의노트", href: "output/greek/week03.html" }
        ] },
        { week: 4, title: "형용사 변화", date: "2026.04", files: [] },
        { week: 5, title: "전치사와 격", date: "2026.04", files: [] },
        { week: 6, title: "동사 기초 — 현재 능동태", date: "2026.04", files: [] },
        { week: 7, title: "동사 — 미완료 과거", date: "2026.04", files: [] },
        { week: 8, title: "중간고사", date: "2026.05", files: [] },
        { week: 9, title: "동사 — 미래", date: "2026.05", files: [] },
        { week: 10, title: "동사 — 부정과거", date: "2026.05", files: [] },
        { week: 11, title: "분사 I", date: "2026.05", files: [] },
        { week: 12, title: "분사 II", date: "2026.06", files: [] },
        { week: 13, title: "부정사와 종속절", date: "2026.06", files: [] },
        { week: 14, title: "신약 본문 독해 실습", date: "2026.06", files: [] },
        { week: 15, title: "기말고사", date: "2026.06", files: [] },
      ]
    },

    min: {
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
        { week: 4, title: "심방과 돌봄 사역", date: "2026.04", files: [] },
        { week: 5, title: "상담 목회 기초", date: "2026.04", files: [] },
        { week: 6, title: "교회 행정과 리더십", date: "2026.04", files: [] },
        { week: 7, title: "교육 목회", date: "2026.04", files: [] },
        { week: 8, title: "중간고사", date: "2026.05", files: [] },
        { week: 9, title: "선교와 전도 사역", date: "2026.05", files: [] },
        { week: 10, title: "소그룹 목회", date: "2026.05", files: [] },
        { week: 11, title: "갈등과 위기 관리", date: "2026.05", files: [] },
        { week: 12, title: "목회자 영성과 자기돌봄", date: "2026.06", files: [] },
        { week: 13, title: "디지털 시대의 목회", date: "2026.06", files: [] },
        { week: 14, title: "한국 교회 현황과 과제", date: "2026.06", files: [] },
        { week: 15, title: "기말고사", date: "2026.06", files: [] },
      ]
    },

    phil: {
      weeks: [
        { week: 1, title: "기독교철학의 학습가이드", date: "2026.03.5.", files: [
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
	    { type: "notes", label: "강의노트", href: "output/기독교철학/week04.html" }
	  ] },
        { week: 5, title: "악의 문제", date: "2026.04", files: [] },
        { week: 6, title: "종교 언어 — 비트겐슈타인", date: "2026.04", files: [] },
        { week: 7, title: "신앙과 이성의 관계", date: "2026.04", files: [] },
        { week: 8, title: "중간고사", date: "2026.05", files: [] },
        { week: 9, title: "종교다원주의", date: "2026.05", files: [] },
        { week: 10, title: "Ricken — 종교철학 I", date: "2026.05", files: [] },
        { week: 11, title: "Ricken — 종교철학 II", date: "2026.05", files: [] },
        { week: 12, title: "기독교와 포스트모더니즘", date: "2026.06", files: [] },
        { week: 13, title: "과학과 종교", date: "2026.06", files: [] },
        { week: 14, title: "기독교 윤리의 철학적 기초", date: "2026.06", files: [] },
        { week: 15, title: "기말고사", date: "2026.06", files: [] },
      ]
    },

    nt: {
      weeks: [
        { week: 1, title: "신구약 중간기 & 수전절", date: "2026.03", files: [
            { type: "notes", label: "강의노트", href: "output/신약성서I/week01.html" }
          ] },
        { week: 2, title: "마태복음 개론 + 신약성서의 세계", date: "2026.03", files: [
            { type: "notes", label: "강의노트", href: "output/신약성서I/week02.html" }
          ] },
        { week: 3, title: "신약성서의 세계와 신약의 문헌들", date: "2026.03", files: [
            { type: "notes", label: "강의노트", href: "output/신약성서I/week03.html" }
          ] },
        { week: 4, title: "산상수훈 II — 율법과 예수", date: "2026.04", files: [] },
        { week: 5, title: "기적 이야기 — 마태복음 8-9장", date: "2026.04", files: [] },
        { week: 6, title: "파송 설교 — 마태복음 10장", date: "2026.04", files: [] },
        { week: 7, title: "비유 설교 — 마태복음 13장", date: "2026.04", files: [] },
        { week: 8, title: "중간고사", date: "2026.05", files: [] },
        { week: 9, title: "교회 설교 — 마태복음 18장", date: "2026.05", files: [] },
        { week: 10, title: "예루살렘 입성과 논쟁", date: "2026.05", files: [] },
        { week: 11, title: "종말 설교 — 마태복음 24-25장", date: "2026.05", files: [] },
        { week: 12, title: "수난 내러티브 I", date: "2026.06", files: [] },
        { week: 13, title: "수난 내러티브 II와 부활", date: "2026.06", files: [] },
        { week: 14, title: "마태복음 신학 종합", date: "2026.06", files: [] },
        { week: 15, title: "기말고사", date: "2026.06", files: [] },
      ]
    },

    hist: {
      weeks: [
        {
          week: 1, title: "기독교 교회사 입문", date: "2026.03.06", files: [
            { type: "notes", label: "강의노트", href: "output/교회사/week01.html" }
          ]
        },
        { week: 2, title: "기독교 형성과 사도시대 I 예수와 유대교의 연관성·분파", date: "2026.03.13", files: [
          { type: "notes", label: "강의노트", href: "output/교회사/week02.html" }
        ] },
        { week: 3, title: "기독교 형성과 사도시대 II", date: "2026.03", files: [
            { type: "notes", label: "강의노트1", href: "output/교회사/week03.html" },
            { type: "notes", label: "강의노트2", href: "output/교회사/week03b.html" }
          ] },
        { week: 4, title: "박해와 순교 — 로마제국과 교회", date: "2026.04", files: [] },
        { week: 5, title: "초대 교부들의 신학", date: "2026.04", files: [] },
        { week: 6, title: "교회 회의와 교리 형성", date: "2026.04", files: [] },
        { week: 7, title: "수도원 운동과 중세 교회", date: "2026.04", files: [] },
        { week: 8, title: "중간고사", date: "2026.05", files: [] },
        { week: 9, title: "스콜라 신학", date: "2026.05", files: [] },
        { week: 10, title: "종교개혁의 배경", date: "2026.05", files: [] },
        { week: 11, title: "루터와 개혁 운동", date: "2026.05", files: [] },
        { week: 12, title: "칼빈과 개혁 교회", date: "2026.06", files: [] },
        { week: 13, title: "침례교의 역사와 신학", date: "2026.06", files: [] },
        { week: 14, title: "미 남침례회(SBC) 논쟁", date: "2026.06", files: [] },
        { week: 15, title: "기말고사", date: "2026.06", files: [] },
      ]
    }
  },

  // ── 헬라어 학습 앱 ──────────────────────────────────────────
  greekTools: [
    {
      name: "헬라어 학습앱1",
      icon: "🔤",
      desc: "알파벳 · 플래시카드 · 퀴즈 · 문법 참고",
      href: "output/greek/night_greek_ver2.html",
      isNew: false
    },
  {
    name: "헬라어 학습앱2",         // ← 새로 추가
    icon: "📖",
    desc: "알파벳 발음 · 단어 · 동사변화 오디오 학습",
    href: "https://drumismylife.github.io/greek-study/",
    isNew: true
  }
  ],

  // ── 관련 자료 ───────────────────────────────────────────────
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