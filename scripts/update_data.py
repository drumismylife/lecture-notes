#!/usr/bin/env python3
import sys, re

DATA_JS = "/Users/macbookpro/Desktop/대학원/lecture-notes/data.js"

COURSE_MAP = {
    "헬라어": "greek",
    "목회학": "min",
    "기독교철학": "phil",
    "신약성서I": "nt",
    "교회사": "hist"
}

def update(course_name, week_str):
    course_key = COURSE_MAP.get(course_name)
    if not course_key:
        print(f"❌ 알 수 없는 과목: {course_name}"); sys.exit(1)

    week_int = int(week_str)
    href = f"output/{course_name}/week{int(week_str):02d}.html"
    new_entry = f'{{ type: "notes", label: "강의노트", href: "{href}" }}'

    text = open(DATA_JS, encoding='utf-8').read()
    course_start = text.find(f'{course_key}:')
    if course_start == -1:
        print(f"❌ 과목 키 없음: {course_key}"); sys.exit(1)

    section = text[course_start:]
    pattern = r'(week:\s*' + str(week_int) + r'\b.*?files:\s*)\[\]'
    m = re.search(pattern, section, re.DOTALL)
    if not m:
        print(f"⚠️  week {week_int} 항목 없음 또는 이미 파일 등록됨"); sys.exit(0)

    new_section = section[:m.start()] + m.group(1) + f'[\n            {new_entry}\n          ]' + section[m.end():]
    open(DATA_JS, 'w', encoding='utf-8').write(text[:course_start] + new_section)
    print(f"✅ data.js 업데이트: {course_name} week{week_str}")

if __name__ == '__main__':
    update(sys.argv[1], sys.argv[2])
