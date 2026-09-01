#!/usr/bin/env python3
from __future__ import annotations
"""
update_data.py — data.js의 (학기, 과목, 주차) files 배열에 강의노트 항목 등록

data.js 구조: SITE_DATA.semesters[] → { id, active, courses: { <키>: { weeks:[...] } } }
모든 편집은 대상 학기(span) 안에서만 수행하여 다른 학기의 동일 과목키를 건드리지 않는다.
학기를 지정하지 않으면 active:true 학기를 대상으로 한다.
"""
import sys, re, json, unicodedata
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_JS = str(SCRIPT_DIR.parent / "data.js")
INDEX_HTML = SCRIPT_DIR.parent / "index.html"
CONFIG_PATH = SCRIPT_DIR / "config.json"


def bump_index_cache_version():
    """index.html의 <script src="data.js?v=...">를 갱신해 브라우저 캐시를 무효화한다.
    data.js 내용이 바뀔 때마다 호출 — 안 부르면 방문자 브라우저가 옛 data.js를 계속 씀."""
    from datetime import date
    if not INDEX_HTML.exists():
        return
    text = INDEX_HTML.read_text(encoding="utf-8")
    m = re.search(r'data\.js\?v=(\d{8})([a-z]?)', text)
    if not m:
        return
    old_date, old_suffix = m.group(1), m.group(2)
    today = date.today().strftime("%Y%m%d")
    if old_date == today:
        new_suffix = chr(ord(old_suffix or "a") + (1 if old_suffix else 0)) if old_suffix else "a"
    else:
        new_suffix = ""
    new_version = f"{today}{new_suffix}"
    new_text = re.sub(r'data\.js\?v=\d{8}[a-z]?', f'data.js?v={new_version}', text)
    if new_text != text:
        INDEX_HTML.write_text(new_text, encoding="utf-8")
        print(f"  캐시 버전 갱신: data.js?v={new_version}")


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


_CONFIG = load_config()
SUBJECTS_CFG = _CONFIG.get("subjects", {})

# config.json의 subjects를 단일 진실 원천(SOT)으로 삼아 과목명→course_key 매핑을 도출
COURSE_MAP = {name: cfg["course_key"] for name, cfg in SUBJECTS_CFG.items()}


def compute_rel_dir(course_name: str, semester_id: str) -> str:
    """학기 고유 ID 기반 결정론적 경로 규칙 (active 상태와 무관):
    - 2026-1(레거시 1학기): output/<output_folder>  ← 기존 배포 URL 영구 보존
    - 그 외 모든 학기(2026-summer, 2026-2, ...): output/<semester_id>/<course_key>
    """
    subj_cfg = SUBJECTS_CFG.get(course_name, {})
    course_key = subj_cfg.get("course_key") or COURSE_MAP.get(course_name)
    if semester_id == "2026-1":
        output_folder = subj_cfg.get("output_folder", course_name)
        return f"output/{output_folder}"
    return f"output/{semester_id}/{course_key}"


# ── 학기 span 유틸 ────────────────────────────────────────────
def active_semester_id(text: str) -> str | None:
    """data.js에서 active:true 학기의 id 반환"""
    m = re.search(r'id:\s*"([^"]+)"(?:(?!id:\s*").)*?active:\s*true', text, re.S)
    return m.group(1) if m else None


def semester_span(text: str, sem_id: str) -> tuple | None:
    """주어진 학기 id 블록의 (start, end) 문자열 인덱스. 다음 학기 id 직전까지."""
    anchor = re.search(r'id:\s*"' + re.escape(sem_id) + r'"', text)
    if not anchor:
        return None
    start = anchor.start()
    nxt = re.search(r'id:\s*"', text[anchor.end():])
    end = anchor.end() + nxt.start() if nxt else len(text)
    return start, end


def resolve_semester(text: str, semester_id: str | None) -> str | None:
    return semester_id or active_semester_id(text)


def update(course_name, week_str, semester_id=None):
    course_key = COURSE_MAP.get(course_name)
    if not course_key:
        print(f"❌ 알 수 없는 과목: {course_name}"); sys.exit(1)

    week_int = int(week_str)

    text = open(DATA_JS, encoding="utf-8").read()

    sem_id = resolve_semester(text, semester_id)
    if not sem_id:
        print("❌ 대상 학기를 찾을 수 없음 (active:true 없음)"); sys.exit(1)

    # 학기 고유 ID 기반 결정론적 경로 (active 상태와 무관 — compute_rel_dir 참조)
    rel_dir = compute_rel_dir(course_name, sem_id)
    href = f"{rel_dir}/week{week_int:02d}.html"
    href = unicodedata.normalize("NFC", href)  # 한글 경로 안전
    new_entry = f'{{ type: "notes", label: "강의노트", href: "{href}" }}'

    span = semester_span(text, sem_id)
    if not span:
        print(f"❌ 학기 블록 없음: {sem_id}"); sys.exit(1)
    s0, s1 = span
    region = text[s0:s1]

    course_start = region.find(f'{course_key}:')
    if course_start == -1:
        print(f"❌ [{sem_id}] 과목 키 없음: {course_key}"); sys.exit(1)

    section = region[course_start:]
    # (?:(?!week:\s*\d).)*? : 다음 week: N 전까지만 매칭 (주차 경계 보존)
    pattern = r'(week:\s*' + str(week_int) + r'\b(?:(?!week:\s*\d).)*?files:\s*)\[\]'
    m = re.search(pattern, section, re.DOTALL)
    if not m:
        print(f"⚠️  [{sem_id}] week {week_int} 항목 없음 또는 이미 파일 등록됨"); sys.exit(0)

    new_section = section[:m.start()] + m.group(1) + f'[\n            {new_entry}\n          ]' + section[m.end():]
    new_region = region[:course_start] + new_section
    open(DATA_JS, "w", encoding="utf-8").write(text[:s0] + new_region + text[s1:])
    bump_index_cache_version()
    print(f"✅ data.js 업데이트: [{sem_id}] {course_name} week{week_str}")


if __name__ == "__main__":
    # 사용법: update_data.py 과목 주차 [학기id]
    sem = sys.argv[3] if len(sys.argv) > 3 else None
    update(sys.argv[1], sys.argv[2], sem)
