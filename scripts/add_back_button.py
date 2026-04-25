#!/usr/bin/env python3
"""
add_back_button.py — 강의노트 HTML 파일에 뒤로가기 버튼 삽입

사용법:
  전체 적용: python3 scripts/add_back_button.py
  단일 파일: python3 scripts/add_back_button.py output/교회사/week07.html
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR   = SCRIPT_DIR.parent

# 버튼을 삽입하지 않을 파일
SKIP_FILES = {"index.html", "night_greek_ver2.html"}

# 중복 삽입 감지용 마커
MARKER = "lnotes-back-btn"

BACK_BUTTON_CSS = """
<style id="lnotes-back-btn-style">
#lnotes-back-btn {
  position: fixed;
  top: 16px;
  left: 16px;
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: rgba(20, 20, 28, 0.82);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(180, 140, 60, 0.35);
  border-radius: 20px;
  color: #c9a84c;
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 13px;
  font-weight: 500;
  text-decoration: none;
  letter-spacing: 0.02em;
  transition: background 0.2s, border-color 0.2s, transform 0.15s;
  cursor: pointer;
}
#lnotes-back-btn:hover {
  background: rgba(30, 28, 20, 0.95);
  border-color: rgba(180, 140, 60, 0.7);
  transform: translateX(-2px);
}
#lnotes-back-btn svg {
  flex-shrink: 0;
}
@media (max-width: 600px) {
  #lnotes-back-btn {
    top: 10px;
    left: 10px;
    padding: 7px 11px;
    font-size: 12px;
  }
}
</style>
"""

BACK_BUTTON_HTML = """<a id="lnotes-back-btn" href="../../index.html">
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <path d="M9 2L4 7L9 12" stroke="#c9a84c" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
  강의 목록
</a>"""


def inject(html_path: Path) -> bool:
    """버튼 삽입. 이미 있으면 False 반환."""
    content = html_path.read_text(encoding="utf-8", errors="ignore")

    if MARKER in content:
        return False  # 이미 삽입됨

    # CSS → </head> 바로 앞에 삽입
    if "</head>" in content:
        content = content.replace("</head>", BACK_BUTTON_CSS + "</head>", 1)
    else:
        return False  # head 없는 파일은 스킵

    # 버튼 HTML → <body> 태그 바로 뒤에 삽입
    if "<body" in content:
        # <body ...> 태그 찾아서 그 뒤에 삽입
        import re
        content = re.sub(
            r'(<body[^>]*>)',
            r'\1' + BACK_BUTTON_HTML,
            content,
            count=1
        )
    else:
        return False

    html_path.write_text(content, encoding="utf-8")
    return True


def run_all():
    html_files = sorted(ROOT_DIR.glob("output/**/*.html"))
    targets = [f for f in html_files if f.name not in SKIP_FILES]

    added, skipped = 0, 0
    for f in targets:
        if inject(f):
            print(f"  ✅ {f.relative_to(ROOT_DIR)}")
            added += 1
        else:
            skipped += 1

    print(f"\n완료: {added}개 추가, {skipped}개 이미 적용됨")


def run_single(path_str: str):
    p = Path(path_str)
    if not p.is_absolute():
        p = ROOT_DIR / p
    if not p.exists():
        print(f"❌ 파일 없음: {p}")
        sys.exit(1)
    if inject(p):
        print(f"✅ 삽입 완료: {p.relative_to(ROOT_DIR)}")
    else:
        print(f"ℹ️  이미 적용됨: {p.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_all()
    else:
        run_single(sys.argv[1])
