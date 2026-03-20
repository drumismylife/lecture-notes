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
          title: "알파벳과 발음 규칙",
          date: "2026.03",
          files: [
            // { type: "notes", label: "강의노트", href: "output/헬라어/week01.html" }
          ]
        },
        { week: 2, title: "명사 변화 I — 제2변화", date: "2026.03", files: [] },
        { week: 3, title: "명사 변화 II — 제1변화", date: "2026.03", files: [] },
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
        { week: 1, title: "목회자의 정체성과 소명", date: "2026.03", files: [] },
        { week: 2, title: "설교의 신학적 기초", date: "2026.03", files: [] },
        { week: 3, title: "예배 신학과 실천", date: "2026.03", files: [] },
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
        { week: 1, title: "기독교철학의 과제와 방법론", date: "2026.03", files: [] },
        { week: 2, title: "신 존재 증명 — 존재론적 논증", date: "2026.03", files: [
            { type: "notes", label: "강의노트", href: "output/기독교철학/week02.html" }
          ] },
        { week: 3, title: "신 존재 증명 — 우주론적 논증", date: "2026.03", files: [] },
        { week: 4, title: "신 존재 증명 — 목적론적 논증", date: "2026.04", files: [] },
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
        { week: 1, title: "마태복음 족보와 탄생 내러티브", date: "2026.03", files: [] },
        { week: 2, title: "세례 요한과 예수의 세례", date: "2026.03", files: [] },
        { week: 3, title: "산상수훈 I — 팔복", date: "2026.03", files: [] },
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
          week: 1,
          title: "기독교 교회사 입문",
          date: "2026.03.06",
          files: [
            { type: "notes", label: "강의노트", href: "output/교회사/week01.html" }
          ]
        },
        { week: 2, title: "기독교 형성과 사도시대 I", date: "2026.03.13", files: [] },
        { week: 3, title: "사도시대 II — 바울과 이방 선교", date: "2026.03", files: [] },
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
      name: "헬라어 학습 앱",
      icon: "🔤",
      desc: "알파벳 · 플래시카드 · 퀴즈 · 문법 참고",
      href: "apps/greek-app.html",
      isNew: false
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
