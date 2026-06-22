#!/usr/bin/env python3
from __future__ import annotations
"""
update_data.py — data.js의 (학기, 과목, 주차) files 배열에 강의노트 항목 등록

data.js 구조: SITE_DATA.semesters[] → { id, active, courses: { <키>: { weeks:[...] } } }
모든 편집은 대상 학기(span) 안에서만 수행하여 다른 학기의 동일 과목키를 건드리지 않는다.
학기를 지정하지 않으면 active:true 학기를 대상으로 한다.
"""
import sys, re, unicodedata

DATA_JS = "/Users/macbookpro/Desktop/대학원/lecture-notes/data.js"

COURSE_MAP = {
    "헬라어": "greek",
    "목회학": "min",
    "기독교철학": "phil",
    "신약성서I": "nt",
    "교회사": "hist",
}

# output 폴더명이 과목명과 다른 경우
OUTPUT_FOLDER_OVERRIDE = {"헬라어": "greek"}


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
    folder = OUTPUT_FOLDER_OVERRIDE.get(course_name, course_name)

    text = open(DATA_JS, encoding="utf-8").read()

    sem_id = resolve_semester(text, semester_id)
    if not sem_id:
        print("❌ 대상 학기를 찾을 수 없음 (active:true 없음)"); sys.exit(1)

    # 활성 학기는 레거시 경로 유지, 그 외 학기는 output/<학기>/<폴더>/ 네임스페이스
    active_id = active_semester_id(text)
    if sem_id != active_id:
        href = f"output/{sem_id}/{folder}/week{week_int:02d}.html"
    else:
        href = f"output/{folder}/week{week_int:02d}.html"
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
    print(f"✅ data.js 업데이트: [{sem_id}] {course_name} week{week_str}")


if __name__ == "__main__":
    # 사용법: update_data.py 과목 주차 [학기id]
    sem = sys.argv[3] if len(sys.argv) > 3 else None
    update(sys.argv[1], sys.argv[2], sem)
