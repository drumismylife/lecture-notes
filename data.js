// ============================================================
// data.js — M.Div 강의 아카이브 데이터
// 매주 강의노트 생성 후 이 파일만 업데이트하면 됩니다.
// ============================================================

const SITE_DATA = {

  // ── 과목별 주차 데이터 ──────────────────────────────────────
  courses: {

    greek: {
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
        { week: 7, title: "동사 — 미완료 과거", date: "2026.04", files: [] },
        { week: 8, title: "중간고사", date: "2026.05", files: [] },
        { week: 9, title: "동사 — 미래", date: "2026.05", files: [] },
        { week: 10, title: "동사 — 부정과거", date: "2026.05", files: [] },
        { week: 11, title: "분사 I", date: "2026.05", files: [] },
        { week: 12, title: "분사 II", date: "2026.06", files: [] },
        { week: 13, title: "부정사와 종속절", date: "2026.06", files: [] },
        { week: 14, title: "신약 본문 독해 실습", date: "2026.06", files: [] },
        { week: 15, title: "기말고사", date: "2026.06", files: [] },
        ] },

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
        { week: 4, title: "목회자의 소명 & 목회와 목회자(2)", date: "2026.03.30", files: [
	  { type: "notes", label: "강의노트", href: "output/목회학/week04.html" }
	] },
        { week: 5, title: "목회자의 정체성과 자기 관리", date: "2026.4.6.", files: [
	  { type: "notes", label: "강의노트", href: "output/목회학/week05.html" }
	] },
        { week: 6, title: "목회자의 영성 관리", date: "2026.04.13.", files: [
	  { type: "notes", label: "강의노트", href: "output/목회학/week06.html" }
	  ] },
        { week: 7, title: "교육 목회", date: "2026.04", files: [] },
        { week: 8, title: "중간고사", date: "2026.05", files: [] },
        { week: 9, title: "선교와 전도 사역", date: "2026.05", files: [] },
        { week: 10, title: "소그룹 목회", date: "2026.05", files: [] },
        { week: 11, title: "갈등과 위기 관리", date: "2026.05", files: [] },
        { week: 12, title: "목회자 영성과 자기돌봄", date: "2026.06", files: [] },
        { week: 13, title: "디지털 시대의 목회", date: "2026.06", files: [] },
        { week: 14, title: "한국 교회 현황과 과제", date: "2026.06", files: [] },
        { week: 15, title: "기말고사", date: "2026.06", files: [] },
        ] },

    phil: {
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
    name: "헬라어 학습앱2",
    icon: "📖",
    desc: "알파벳 발음 · 단어 · 동사변화 오디오 학습",
    href: "https://drumismylife.github.io/greek-study/",
    isNew: true
  },
  {
    name: "헬라어 현재-수동 외우기 노래1",
    icon: "🎶",
    desc: "현재-수동 외우기 노래",
    href: "output/greek/현재-수동1.mp3",
    isNew: true
  },
  {
    name: "헬라어 현재-수동 외우기 노래2",
    icon: "🎶",
    desc: "현재-수동 외우기 노래",
    href: "output/greek/현재-수동2.mp3",
    isNew: true
  },
  {
    name: "헬라어 미래-수동 외우기 노래1",
    icon: "🎶",
    desc: "미래-수동 외우기 노래",
    href: "output/greek/미래-수동1.mp3",
    isNew: true
  },
  {
    name: "헬라어 미래-수동 외우기 노래2",
    icon: "🎶",
    desc: "미래-수동 외우기 노래",
    href: "output/greek/미래-수동2.mp3",
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
