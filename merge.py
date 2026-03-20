#!/usr/bin/env python3
"""
merge.py — 마크다운 강의노트를 HTML로 합성하는 스크립트
사용법: python3 scripts/merge.py data/신약성서/week01.md
"""

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR   = SCRIPT_DIR.parent
TEMPLATE   = ROOT_DIR / "template" / "lecture.html"


# ── 1. 마크다운 파일 파싱 ──────────────────────────────────────────

def parse_frontmatter(text):
    """YAML frontmatter (--- ... ---) 에서 메타 정보 추출"""
    meta = {}
    match = re.search(r'^---\n(.*?)\n---', text, re.DOTALL)
    if match:
        for line in match.group(1).splitlines():
            if ':' in line:
                key, _, val = line.partition(':')
                meta[key.strip()] = val.strip()
    return meta


def parse_sections(text):
    """## 섹션 헤더 기준으로 내용 분리"""
    # frontmatter 제거
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)

    content = ''
    notes   = ''

    content_match = re.search(
        r'## 강의 내용\n(.*?)(?=\n## |\Z)', text, re.DOTALL)
    notes_match = re.search(
        r'## 시사점.*?\n(.*?)(?=\n## |\Z)', text, re.DOTALL)

    if content_match:
        content = content_match.group(1).strip()
    if notes_match:
        notes = notes_match.group(1).strip()

    return content, notes


# ── 2. 마크다운 → HTML 변환 ───────────────────────────────────────

def md_to_prose(text):
    """강의 내용: 문단 단위 HTML 변환"""
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*',     r'<em>\1</em>', text)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return '\n'.join(f'<p>{p}</p>' for p in paragraphs)


def md_to_notes(text):
    """시사점: - 리스트 항목을 <li>로 변환"""
    items = re.findall(r'^[-*]\s+(.+)$', text, re.MULTILINE)
    if not items:
        # 리스트 마커 없으면 줄 단위로 처리
        items = [line.strip() for line in text.splitlines() if line.strip()]
    return '\n'.join(f'<li>{item}</li>' for item in items)


def keywords_to_tags(keywords_str):
    """쉼표 구분 키워드를 태그 span으로 변환"""
    tags = [k.strip() for k in keywords_str.split(',') if k.strip()]
    return '\n'.join(f'<span class="keyword-tag">{tag}</span>' for tag in tags)


# ── 3. 합성 및 저장 ───────────────────────────────────────────────

def merge(md_path_str):
    md_path = Path(md_path_str).resolve()

    if not md_path.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {md_path}")
        sys.exit(1)

    if not TEMPLATE.exists():
        print(f"❌ 템플릿을 찾을 수 없습니다: {TEMPLATE}")
        sys.exit(1)

    md_text      = md_path.read_text(encoding='utf-8')
    template_str = TEMPLATE.read_text(encoding='utf-8')

    meta             = parse_frontmatter(md_text)
    content_md, notes_md = parse_sections(md_text)

    result = template_str \
        .replace('{{COURSE}}',   meta.get('course',   '(과목명 없음)')) \
        .replace('{{WEEK}}',     meta.get('week',     '(주차 없음)')) \
        .replace('{{DATE}}',     meta.get('date',     '')) \
        .replace('{{KEYWORDS}}', keywords_to_tags(meta.get('keywords', ''))) \
        .replace('{{CONTENT}}',  md_to_prose(content_md)) \
        .replace('{{NOTES}}',    md_to_notes(notes_md))

    # output/과목명/ 폴더에 저장
    subject_name = md_path.parent.name
    out_dir  = ROOT_DIR / "output" / subject_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / md_path.with_suffix('.html').name
    out_path.write_text(result, encoding='utf-8')

    print(f"✅ 완료: {out_path}")
    print(f"   과목: {meta.get('course', '?')} / {meta.get('week', '?')}")


# ── 4. 전체 일괄 처리 옵션 ───────────────────────────────────────

def merge_all():
    """data/ 폴더 아래 모든 .md 파일을 일괄 변환"""
    data_dir = ROOT_DIR / "data"
    md_files = list(data_dir.rglob("*.md"))
    if not md_files:
        print("⚠️  data/ 폴더에 .md 파일이 없습니다.")
        return
    print(f"📚 {len(md_files)}개 파일 변환 시작...\n")
    for f in sorted(md_files):
        merge(str(f))
    print(f"\n🎉 전체 완료!")


# ── 실행 진입점 ──────────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("사용법:")
        print("  단일 파일: python3 scripts/merge.py data/신약성서/week01.md")
        print("  전체 변환: python3 scripts/merge.py --all")
        sys.exit(0)

    if sys.argv[1] == '--all':
        merge_all()
    else:
        merge(sys.argv[1])
