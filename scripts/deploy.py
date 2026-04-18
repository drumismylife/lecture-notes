#!/usr/bin/env python3
"""
deploy.py — HTML 파일을 output/ 에 넣은 후 data.js 업데이트 + git push

사용법:
  python3 scripts/deploy.py 기독교철학 07 2026.04.16   ← 첫 번째 자료
  python3 scripts/deploy.py 기독교철학 07b 2026.04.16  ← 같은 주차 추가 자료
  python3 scripts/deploy.py 신약성서I 07               ← 날짜 생략 시 오늘 날짜 자동입력
"""

import re
import sys
import subprocess
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR   = SCRIPT_DIR.parent

sys.path.insert(0, str(SCRIPT_DIR))
from update_data import update as update_data_js, COURSE_MAP

OUTPUT_FOLDER_OVERRIDE = {"헬라어": "greek"}
COURSE_NAMES = ", ".join(COURSE_MAP.keys())


def extract_title_from_html(html_path: Path) -> str:
    """HTML에서 강의 제목 추출 (여러 형식 지원)"""
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    patterns = [
        r'class="header-title"[^>]*>(.*?)<',
        r'class="[^"]*header[^"]*title[^"]*"[^>]*>(.*?)<',
        r'<h1[^>]*>(.*?)</h1>',
        r'<title[^>]*>[^—–-]*[—–-]\s*(.*?)</title>',
    ]
    for pat in patterns:
        m = re.search(pat, html, re.DOTALL | re.IGNORECASE)
        if m:
            title = re.sub(r'<[^>]+>', ' ', m.group(1))
            title = re.sub(r'\s+', ' ', title).strip()
            if title:
                return title
    return ""


def _update_field_in_data_js(subject: str, week_num: int, field: str, value: str):
    """data.js 해당 주차의 특정 필드 업데이트 (주차 경계 넘지 않음)"""
    course_key = COURSE_MAP[subject]
    data_js = ROOT_DIR / "data.js"
    text = data_js.read_text(encoding="utf-8")

    course_start = text.find(f'{course_key}:')
    if course_start == -1:
        return

    section = text[course_start:]
    pattern = (
        r'(week:\s*' + str(week_num) +
        r'\b(?:(?!week:\s*\d).)*?' +
        field + r':\s*)"[^"]*"'
    )
    new_section, count = re.subn(
        pattern, r'\1"' + value + '"', section, count=1, flags=re.DOTALL
    )
    if count:
        data_js.write_text(text[:course_start] + new_section, encoding="utf-8")


def update_title_in_data_js(subject: str, week_num: int, title: str):
    _update_field_in_data_js(subject, week_num, "title", title)
    print(f"  제목 업데이트: {title}")


def update_date_in_data_js(subject: str, week_num: int, lecture_date: str):
    _update_field_in_data_js(subject, week_num, "date", lecture_date)
    print(f"  날짜 업데이트: {lecture_date}")


def append_file_to_data_js(subject: str, week_num: int, href: str, label: str):
    """이미 파일이 있는 주차의 files 배열에 항목 추가 (중복 방지)"""
    course_key = COURSE_MAP[subject]
    data_js = ROOT_DIR / "data.js"
    text = data_js.read_text(encoding="utf-8")

    # 이미 등록됐는지 확인
    if href in text:
        print(f"  ℹ️  이미 등록됨: {href}")
        return

    course_start = text.find(f'{course_key}:')
    if course_start == -1:
        return

    section = text[course_start:]

    # 해당 주차의 files 배열 닫는 ] 위치 찾기 (주차 경계 내에서)
    week_pattern = r'week:\s*' + str(week_num) + r'\b(?:(?!week:\s*\d).)*?files:\s*\['
    m = re.search(week_pattern, section, re.DOTALL)
    if not m:
        print(f"  ❌ week {week_num} files 배열을 찾을 수 없음")
        return

    # files: [ 이후 닫는 ] 찾기
    files_start = course_start + m.end()
    depth = 1
    i = files_start
    while i < len(text) and depth > 0:
        if text[i] == '[':
            depth += 1
        elif text[i] == ']':
            depth -= 1
        i += 1
    files_end = i - 1  # ] 위치

    new_entry = f'\n            {{ type: "notes", label: "{label}", href: "{href}" }}'
    # 기존 마지막 항목 뒤에 쉼표 추가 후 새 항목 삽입
    before_close = text[:files_end].rstrip()
    new_text = before_close + ',' + new_entry + '\n          ' + text[files_end:]
    data_js.write_text(new_text, encoding="utf-8")
    print(f"  파일 추가: {label} ({href})")


def parse_week_arg(week_arg: str) -> tuple:
    """'07' → (7, ''), '07b' → (7, 'b'), '07c' → (7, 'c')"""
    m = re.match(r'^0*(\d+)([a-z]?)$', week_arg.strip().lower())
    if not m:
        return None, None
    return int(m.group(1)), m.group(2)


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("사용법: python3 scripts/deploy.py [과목명] [주차] [날짜(선택)]")
        print(f"  과목명: {COURSE_NAMES}")
        print("  예시:   python3 scripts/deploy.py 기독교철학 07 2026.04.16")
        print("          python3 scripts/deploy.py 기독교철학 07b 2026.04.16")
        print("          python3 scripts/deploy.py 기독교철학 07   ← 오늘 날짜 자동")
        sys.exit(1)

    subject  = sys.argv[1]
    week_num, variant = parse_week_arg(sys.argv[2])

    if week_num is None:
        print(f"❌ 주차 형식 오류: {sys.argv[2]} (07 또는 07b 형식)")
        sys.exit(1)

    if len(sys.argv) == 4:
        lecture_date = sys.argv[3]
    else:
        today = date.today()
        lecture_date = f"{today.year}.{today.month:02d}.{today.day:02d}"

    if subject not in COURSE_MAP:
        print(f"❌ 알 수 없는 과목: {subject}")
        print(f"   사용 가능: {COURSE_NAMES}")
        sys.exit(1)

    out_folder = OUTPUT_FOLDER_OVERRIDE.get(subject, subject)
    file_suffix = f"week{week_num:02d}{variant}.html"
    html_path = ROOT_DIR / "output" / out_folder / file_suffix

    if not html_path.exists():
        print(f"❌ HTML 파일이 없습니다: output/{out_folder}/{file_suffix}")
        print(f"   해당 경로에 파일을 먼저 저장하세요.")
        sys.exit(1)

    variant_label = f" ({variant.upper()})" if variant else ""
    print(f"📄 [{subject}] Week {week_num:02d}{variant_label} 배포 시작\n")

    print("[1/2] data.js 업데이트...")

    title = extract_title_from_html(html_path)
    if not title:
        title = file_suffix.replace(".html", "")
        print(f"  ⚠️  제목 추출 실패 → '{title}' 사용")

    href = f"output/{out_folder}/{file_suffix}"

    if not variant:
        # 첫 번째 자료: title·date 업데이트 + files: [] 등록
        update_title_in_data_js(subject, week_num, title)
        update_date_in_data_js(subject, week_num, lecture_date)
        try:
            update_data_js(subject, str(week_num))
        except SystemExit as e:
            if e.code != 0:
                print("  ⚠️  data.js 파일 등록 실패")
                sys.exit(1)
    else:
        # 추가 자료 (b, c ...): 기존 배열에 append, date는 업데이트하지 않음
        append_file_to_data_js(subject, week_num, href, title)

    # 2단계: git push
    print("[2/2] GitHub 업로드...")
    commit_msg = f"강의노트 업데이트: {subject} week{week_num:02d}{variant}"
    cmds = [
        ["git", "-C", str(ROOT_DIR), "add", "output/", "data.js"],
        ["git", "-C", str(ROOT_DIR), "commit", "-m", commit_msg],
        ["git", "-C", str(ROOT_DIR), "push"],
    ]

    for cmd in cmds:
        result = subprocess.run(cmd, capture_output=True, text=True)
        label  = " ".join(cmd[3:])
        if result.returncode != 0:
            if "nothing to commit" in result.stdout + result.stderr:
                print(f"  ℹ️  변경 없음 (이미 최신)")
            else:
                print(f"  ❌ 실패: {label}")
                print(f"     {result.stderr.strip()}")
                sys.exit(1)
        else:
            print(f"  ✅ {label}")

    print(f"\n🎉 완료! 잠시 후 GitHub Pages에서 확인하세요.")


if __name__ == "__main__":
    main()
