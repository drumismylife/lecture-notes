#!/usr/bin/env python3
"""
merge.py — 마크다운 강의노트를 고품질 HTML로 변환
사용법:
  단일 파일: python3 scripts/merge.py data/신약성서/week01.md
  전체 변환: python3 scripts/merge.py --all
"""

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR   = SCRIPT_DIR.parent

# ══════════════════════════════════════════════════════════════
# 1. CSS (완전 내장)
# ══════════════════════════════════════════════════════════════

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@300;400;600;700;900&family=Noto+Sans+KR:wght@300;400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root {
  --ink:#1a1208; --parchment:#f5f0e8; --warm-white:#faf7f2;
  --gold:#b8860b; --gold-light:#d4a017; --gold-pale:#f0e4b8;
  --rust:#8b3a1a; --deep-brown:#3d2008; --mid-brown:#6b3f1a;
  --border:#c8a96e; --shadow:rgba(61,32,8,0.15);
}
*{margin:0;padding:0;box-sizing:border-box;}
body{background:var(--parchment);background-image:radial-gradient(ellipse at 20% 10%,rgba(184,134,11,.06) 0%,transparent 50%),radial-gradient(ellipse at 80% 90%,rgba(139,58,26,.05) 0%,transparent 50%);font-family:'Noto Sans KR',sans-serif;color:var(--ink);min-height:100vh;padding:2rem 1rem 4rem;}
.page{max-width:860px;margin:0 auto;opacity:0;animation:pageReveal .8s ease forwards;}
@keyframes pageReveal{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
.header{text-align:center;padding:3rem 2rem 2.5rem;position:relative;margin-bottom:.5rem;}
.header::before,.header::after{content:'';display:block;height:2px;background:linear-gradient(90deg,transparent,var(--gold),transparent);margin:.8rem auto;width:60%;}
.course-label{font-family:'Noto Serif KR',serif;font-size:.78rem;font-weight:600;letter-spacing:.3em;color:var(--mid-brown);text-transform:uppercase;margin-bottom:.8rem;}
.header h1{font-family:'Noto Serif KR',serif;font-size:2.2rem;font-weight:900;color:var(--deep-brown);line-height:1.3;margin-bottom:.6rem;}
.header h1 span{color:var(--gold);}
.header-meta{font-size:.82rem;color:var(--mid-brown);font-weight:300;letter-spacing:.05em;}
.week-badge{display:inline-block;background:var(--deep-brown);color:var(--gold-pale);font-family:'Noto Serif KR',serif;font-size:.72rem;font-weight:700;letter-spacing:.15em;padding:.3rem 1rem;border-radius:2px;margin-bottom:1rem;}
.section{background:var(--warm-white);border:1px solid var(--border);border-radius:4px;margin-bottom:1.6rem;overflow:hidden;box-shadow:0 2px 12px var(--shadow);opacity:0;animation:sectionIn .6s ease forwards;}
.section:nth-child(1){animation-delay:.1s}.section:nth-child(2){animation-delay:.2s}.section:nth-child(3){animation-delay:.3s}.section:nth-child(4){animation-delay:.4s}.section:nth-child(5){animation-delay:.5s}.section:nth-child(6){animation-delay:.6s}
@keyframes sectionIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.section-header{display:flex;align-items:center;gap:.7rem;padding:.9rem 1.4rem;background:linear-gradient(135deg,var(--deep-brown) 0%,var(--mid-brown) 100%);color:var(--gold-pale);}
.section-icon{font-size:1.1rem;flex-shrink:0;}
.section-header h2{font-family:'Noto Serif KR',serif;font-size:.95rem;font-weight:700;letter-spacing:.04em;}
.section-body{padding:1.4rem;}
table{width:100%;border-collapse:collapse;font-size:.88rem;}
thead tr{background:var(--gold-pale);border-bottom:2px solid var(--gold);}
thead th{padding:.6rem 1rem;text-align:left;font-family:'Noto Serif KR',serif;font-weight:700;color:var(--deep-brown);font-size:.82rem;letter-spacing:.05em;}
tbody tr{border-bottom:1px solid #e8dcc8;transition:background .15s;}
tbody tr:hover{background:rgba(212,160,23,.06);}
tbody tr:last-child{border-bottom:none;}
tbody td{padding:.65rem 1rem;color:var(--ink);line-height:1.55;vertical-align:top;}
tbody td:first-child{font-weight:600;color:var(--mid-brown);font-size:.84rem;}
.prose p{font-size:.9rem;line-height:1.8;color:var(--ink);margin-bottom:.9rem;}
.prose p:last-child{margin-bottom:0;}
.prose strong{font-weight:700;color:var(--deep-brown);}
.prose em{color:var(--mid-brown);font-style:normal;font-weight:500;}
.callout{border-left:3px solid var(--gold);background:linear-gradient(135deg,rgba(240,228,184,.35),rgba(240,228,184,.1));padding:1rem 1.2rem;border-radius:0 4px 4px 0;margin-top:1rem;}
.callout-title{font-family:'Noto Serif KR',serif;font-size:.82rem;font-weight:700;color:var(--rust);margin-bottom:.5rem;letter-spacing:.05em;}
.callout p{font-size:.88rem;line-height:1.7;color:var(--ink);}
.alert{display:flex;gap:.8rem;align-items:flex-start;background:rgba(139,58,26,.06);border:1px solid rgba(139,58,26,.25);border-radius:4px;padding:.9rem 1.1rem;margin-top:1rem;font-size:.87rem;line-height:1.65;}
.alert-icon{font-size:1.1rem;flex-shrink:0;margin-top:.05rem;}
.alert strong{color:var(--rust);}
.key-points{display:flex;flex-direction:column;gap:.9rem;}
.key-point{display:flex;gap:1rem;align-items:flex-start;padding:.9rem 1.1rem;background:var(--parchment);border-radius:4px;border:1px solid #ddd0b0;transition:transform .15s,box-shadow .15s;}
.key-point:hover{transform:translateX(3px);box-shadow:-3px 0 0 var(--gold),0 2px 8px var(--shadow);}
.key-num{font-family:'Noto Serif KR',serif;font-size:1.5rem;font-weight:900;color:var(--gold);line-height:1;flex-shrink:0;min-width:2rem;opacity:.7;}
.key-text strong{display:block;font-size:.9rem;font-weight:700;color:var(--deep-brown);margin-bottom:.25rem;font-family:'Noto Serif KR',serif;}
.key-text p{font-size:.84rem;line-height:1.65;color:#4a3820;}
.quote-block{border:1px solid var(--border);border-radius:4px;padding:1.2rem 1.4rem;background:rgba(248,243,232,.6);position:relative;margin-bottom:1rem;}
.quote-block::before{content:'\201C';font-family:'Noto Serif KR',serif;font-size:4rem;color:var(--gold);opacity:.3;position:absolute;top:-.5rem;left:.8rem;line-height:1;}
.quote-block p{font-family:'Noto Serif KR',serif;font-size:1rem;font-weight:600;color:var(--deep-brown);line-height:1.7;padding-left:1.5rem;}
.quote-sub{font-size:.82rem;color:var(--mid-brown);padding-left:1.5rem;margin-top:.4rem;}
.note-list{list-style:none;padding:0;}
.note-list li{padding:.75rem 1rem .75rem 2.4rem;margin-bottom:.5rem;background:#f0f4fa;border-left:3px solid #4a6fa5;border-radius:0 4px 4px 0;font-size:.88rem;line-height:1.65;position:relative;}
.note-list li::before{content:'→';position:absolute;left:.8rem;color:#4a6fa5;font-weight:700;}
.keyword-list{display:flex;flex-wrap:wrap;gap:.5rem;}
.keyword-tag{display:inline-block;background:var(--deep-brown);color:var(--gold-pale);font-family:'JetBrains Mono',monospace;font-size:.78rem;padding:.25rem .75rem;border-radius:2px;letter-spacing:.04em;}
.next-week{text-align:center;padding:1.5rem;background:linear-gradient(135deg,var(--deep-brown),var(--mid-brown));border-radius:4px;color:var(--gold-pale);margin-bottom:1.6rem;}
.next-week .label{font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;opacity:.7;margin-bottom:.4rem;}
.next-week h3{font-family:'Noto Serif KR',serif;font-size:1.05rem;font-weight:700;margin-bottom:.3rem;}
.next-week p{font-size:.82rem;opacity:.75;}
.ornament{text-align:center;color:var(--gold);font-size:1.1rem;letter-spacing:.5rem;margin:.2rem 0;opacity:.5;}
@media(max-width:600px){.header h1{font-size:1.6rem;}tbody td:first-child{white-space:normal;}}
"""

# ══════════════════════════════════════════════════════════════
# 2. 유틸
# ══════════════════════════════════════════════════════════════

def parse_frontmatter(text):
    meta = {}
    m = re.search(r'^---\n(.*?)\n---', text, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                k, _, v = line.partition(':')
                meta[k.strip()] = v.strip()
    return meta

def strip_frontmatter(text):
    return re.sub(r'^---\n.*?\n---\n?', '', text, flags=re.DOTALL).strip()

def inline_md(t):
    t = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\*(.*?)\*',     r'<em>\1</em>', t)
    t = re.sub(r'`(.*?)`',       r'<code>\1</code>', t)
    return t

ICONS = {
    '강의 핵심 정보':'📚','강의정보':'📚',
    '강의 내용':'📖',
    '핵심 포인트':'🔑','핵심포인트':'🔑',
    '시사점':'✏️','준비사항':'✏️','시사점 / 준비사항':'✏️',
    '특별 언급':'🏛️','특별언급':'🏛️',
    '핵심 단어':'🔤','핵심단어':'🔤','키워드':'🔤',
}
def get_icon(title):
    for k,v in ICONS.items():
        if k in title: return v
    return '📋'

# ══════════════════════════════════════════════════════════════
# 3. 컴포넌트 렌더러
# ══════════════════════════════════════════════════════════════

def render_table(lines):
    rows = []
    for l in lines:
        l = l.strip()
        if l.startswith('|') and not re.match(r'^\|[-| ]+\|$', l):
            cells = [c.strip() for c in l.strip('|').split('|')]
            if len(cells) >= 2:
                rows.append(cells)
    if not rows: return ''
    has_header = rows[0][0] in ('항목','구분','내용','Item','분류')
    html = '<table>'
    start = 0
    if has_header:
        html += '<thead><tr>'+''.join(f'<th>{c}</th>' for c in rows[0])+'</tr></thead>'
        start = 1
    html += '<tbody>'
    for row in rows[start:]:
        html += '<tr>'+''.join(f'<td>{inline_md(c)}</td>' for c in row)+'</tr>'
    html += '</tbody></table>'
    return html

def render_key_points(lines):
    items = []
    for l in lines:
        m = re.match(r'^\d+\.\s*(.*)', l.strip())
        if m:
            content = m.group(1)
            title, _, desc = content.partition('|') if '|' in content else (content,'','')
            title = re.sub(r'\*\*(.*?)\*\*', r'\1', title).strip()
            items.append((title, inline_md(desc.strip())))
    if not items: return ''
    html = '<div class="key-points">'
    for n,(title,desc) in enumerate(items,1):
        html += f'<div class="key-point"><div class="key-num">{n:02d}</div><div class="key-text"><strong>{title}</strong><p>{desc}</p></div></div>'
    html += '</div>'
    return html

def render_prose_with_extras(lines):
    html = ''
    buf  = []

    def flush():
        nonlocal html, buf
        if buf:
            html += f'<p>{inline_md(" ".join(buf))}</p>\n'
            buf = []

    for line in lines:
        # 인용
        if line.startswith('>'):
            flush()
            q = line.lstrip('> ').strip()
            attr = ''
            m = re.search(r'[—–-]\s*(.+)$', q)
            if m:
                attr = m.group(1).strip()
                q    = q[:m.start()].strip().strip('""\'"\'')
            attr_html = ("<div class='quote-sub'>— " + attr + "</div>") if attr else ""
            html += f'<div class="quote-block"><p>{q}</p>{attr_html}</div>\n'
        # 콜아웃
        elif re.match(r'^\[!(NOTE|TIP)\]', line):
            flush()
            c = re.sub(r'^\[!(?:NOTE|TIP)\]\s*','',line)
            title, _, body = c.partition('|') if '|' in c else ('참고','',c)
            html += f'<div class="callout"><div class="callout-title">💡 {inline_md(title.strip())}</div><p>{inline_md(body.strip())}</p></div>\n'
        # 경고
        elif line.startswith('[!WARN]'):
            flush()
            c = re.sub(r'^\[!WARN\]\s*','',line)
            html += f'<div class="alert"><span class="alert-icon">⚠️</span><div>{inline_md(c)}</div></div>\n'
        elif not line.strip():
            flush()
        else:
            buf.append(line.strip())

    flush()
    return f'<div class="prose">{html}</div>' if html else ''

def render_notes(lines):
    items = [re.sub(r'^[-*]\s*','',l).strip() for l in lines if re.match(r'^[-*]\s',l.strip())]
    if not items: return ''
    return '<ul class="note-list">'+''.join(f'<li>{inline_md(i)}</li>' for i in items)+'</ul>'

def render_keywords(text):
    tags = [k.strip() for k in text.split(',') if k.strip()]
    return '<div class="keyword-list">'+''.join(f'<span class="keyword-tag">{t}</span>' for t in tags)+'</div>'

# ══════════════════════════════════════════════════════════════
# 4. 섹션 → HTML
# ══════════════════════════════════════════════════════════════

def section_to_html(title, lines):
    icon     = get_icon(title)
    stripped = [l for l in lines if l.strip()]

    has_table     = any(l.strip().startswith('|') for l in stripped)
    has_keypoints = any(re.match(r'^\d+\.', l.strip()) for l in stripped)
    has_list      = any(re.match(r'^[-*]\s', l.strip()) for l in stripped)
    is_keywords   = any(k in title for k in ('핵심 단어','핵심단어','키워드'))

    if is_keywords:
        body_html = render_keywords(', '.join(stripped))
    elif has_table:
        body_html = render_table(stripped)
        extras = [l for l in stripped if not l.strip().startswith('|')]
        if extras:
            body_html += render_prose_with_extras(extras)
    elif has_keypoints:
        body_html = render_key_points(stripped)
        extras = [l for l in stripped if l.startswith('[!') or l.startswith('>')]
        if extras:
            body_html += render_prose_with_extras(extras)
    elif has_list and not any(l.startswith('>') or l.startswith('[!') for l in stripped):
        note_lines  = [l for l in stripped if re.match(r'^[-*]\s',l.strip())]
        extra_lines = [l for l in stripped if l.strip().startswith('[!') or l.strip().startswith('>')]
        body_html   = render_notes(note_lines)
        if extra_lines:
            body_html += render_prose_with_extras(extra_lines)
    else:
        body_html = render_prose_with_extras(stripped)

    return f'''<div class="section">
  <div class="section-header"><span class="section-icon">{icon}</span><h2>{title}</h2></div>
  <div class="section-body">{body_html}</div>
</div>'''

# ══════════════════════════════════════════════════════════════
# 5. HTML 조립
# ══════════════════════════════════════════════════════════════

def parse_sections(text):
    sections, cur_title, cur_lines = [], None, []
    for line in text.splitlines():
        if line.startswith('## '):
            if cur_title is not None:
                sections.append((cur_title, cur_lines))
            cur_title, cur_lines = line[3:].strip(), []
        else:
            if cur_title is not None:
                cur_lines.append(line)
    if cur_title is not None:
        sections.append((cur_title, cur_lines))
    return sections

def build_html(meta, sections):
    course    = meta.get('course','강의명')
    week      = meta.get('week','')
    date      = meta.get('date','')
    professor = meta.get('professor','')
    schedule  = meta.get('schedule','')
    next_week = meta.get('next_week','')
    next_date = meta.get('next_date','')
    next_prep = meta.get('next_prep','')

    words = course.strip().split()
    title_html = (' '.join(words[:-1])+f' <span>{words[-1]}</span>') if len(words)>1 else course
    badge_str  = ' · '.join(p for p in [week,date] if p)
    meta_parts = [p for p in [professor,schedule] if p]
    meta_str   = ' · '.join(meta_parts)

    secs_html  = '\n'.join(section_to_html(t,l) for t,l in sections)

    next_html = ''
    if next_week:
        next_html = f'''<div class="next-week">
  <div class="label">Next Week · {next_date}</div>
  <h3>{next_week}</h3>
  {"<p>"+next_prep+"</p>" if next_prep else ""}
</div>'''

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{course} — {week}</title>
<style>{CSS}</style>
</head>
<body>
<div class="page">
  <div class="header">
    <div class="week-badge">{badge_str}</div>
    <div class="course-label">한국침례신학대학교 · {course}</div>
    <h1>{title_html}</h1>
    {"<div class='header-meta'>"+meta_str+"</div>" if meta_str else ""}
  </div>
  <div class="ornament">✦ ✦ ✦</div>
  {secs_html}
  {next_html}
</div>
</body>
</html>"""

# ══════════════════════════════════════════════════════════════
# 6. 실행
# ══════════════════════════════════════════════════════════════

def merge(md_path_str):
    md_path = Path(md_path_str).resolve()
    if not md_path.exists():
        print(f"❌ 파일 없음: {md_path}"); sys.exit(1)

    text     = md_path.read_text(encoding='utf-8')
    meta     = parse_frontmatter(text)
    body     = strip_frontmatter(text)
    sections = parse_sections(body)
    html     = build_html(meta, sections)

    out_dir  = ROOT_DIR / "output" / md_path.parent.name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / md_path.with_suffix('.html').name
    out_path.write_text(html, encoding='utf-8')
    print(f"✅ 완료: {out_path}")
    print(f"   {meta.get('course','?')} / {meta.get('week','?')}")

def merge_all():
    files = sorted((ROOT_DIR/"data").rglob("*.md"))
    if not files:
        print("⚠️  data/ 에 .md 파일이 없습니다."); return
    print(f"📚 {len(files)}개 변환 시작...\n")
    for f in files: merge(str(f))
    print("\n🎉 전체 완료!")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("사용법:\n  단일: python3 scripts/merge.py data/교회사/week01.md\n  전체: python3 scripts/merge.py --all")
        sys.exit(0)
    if sys.argv[1] == '--all': merge_all()
    else: merge(sys.argv[1])
