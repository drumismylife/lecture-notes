#!/usr/bin/env python3
"""
bible_fetch.py — 개역개정(bskorea, version=GAE) 장 단위 fetch + parse. FAIL LOUD.

사용:
  python3 scripts/bible_fetch.py "욘 4:11"          # 한 절
  python3 scripts/bible_fetch.py "합 2:3-5"         # 범위
  python3 scripts/bible_fetch.py hab 2              # 장 전체 (book code 또는 한글명, 장)
  python3 scripts/bible_fetch.py "욘 4:11" --json
  (옵션) --cache-dir DIR : 검증을 통과한 장만 DIR/<code>_<chap>.json 으로 저장·재사용

모듈:
  from bible_fetch import fetch_chapter, fetch_verses, resolve_book, BibleFetchError
  fetch_chapter("hab", 2) -> {1: "...", ..., 20: "..."}   (검증 통과분만 반환)
  fetch_verses("욘 4:11") -> {11: "..."}

불변 규칙 (D-2, 2026-11-04):
  1. sec=N 을 URL에 절대 붙이지 않는다. (sec=N 이면 N절의 번호 span 이
     `<span class="number"><a name=focus></a>N` 로 바뀌어, 번호 span 만 찾는 파서가 N절을 조용히 버린다.)
     그래도 방어적으로 focus anchor 는 허용해 파싱한다.
  2. 아래는 모두 BibleFetchError (조용한 통과 없음):
     - 알 수 없는 책 코드/이름 (예: 요나는 jon 이 아니라 jnh — jon 은 빈 페이지가 온다)
     - 페이지가 요청한 책/장(initBook/initChap)과 다름, 또는 개역개정이 아님
     - 절이 하나도 없음(빈 페이지·차단 페이지)
     - 절 번호가 1..N 연속이 아님(누락·중복·역순)
     - 본문이 비었거나 사이트 JS/HTML 꼬리 흔적이 남음
  3. 사이트의 JS 꼬리 텍스트(마지막 절 뒤 </div>·<script>...)는 절 span 종료 지점에서 잘라낸다.
"""
from __future__ import annotations
import html as html_lib
import json
import os
import re
import sys
import urllib.request

BASE_URL = "https://www.bskorea.or.kr/bible/korbibReadpage.php?version=GAE&book={book}&chap={chap}"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


class BibleFetchError(RuntimeError):
    pass


# 66권: 코드(bskorea 실측 2026-11-04: 66코드 모두 chap=1 에서 절 반환, 'jon' 은 0절) -> (한글 정식명, 약어들)
_BOOKS = [
    ("gen", "창세기", "창"), ("exo", "출애굽기", "출"), ("lev", "레위기", "레"),
    ("num", "민수기", "민"), ("deu", "신명기", "신"), ("jos", "여호수아", "수"),
    ("jdg", "사사기", "삿"), ("rut", "룻기", "룻"), ("1sa", "사무엘상", "삼상"),
    ("2sa", "사무엘하", "삼하"), ("1ki", "열왕기상", "왕상"), ("2ki", "열왕기하", "왕하"),
    ("1ch", "역대상", "대상"), ("2ch", "역대하", "대하"), ("ezr", "에스라", "스"),
    ("neh", "느헤미야", "느"), ("est", "에스더", "에"), ("job", "욥기", "욥"),
    ("psa", "시편", "시"), ("pro", "잠언", "잠"), ("ecc", "전도서", "전"),
    ("sng", "아가", "아"), ("isa", "이사야", "사"), ("jer", "예레미야", "렘"),
    ("lam", "예레미야애가", "애"), ("ezk", "에스겔", "겔"), ("dan", "다니엘", "단"),
    ("hos", "호세아", "호"), ("jol", "요엘", "욜"), ("amo", "아모스", "암"),
    ("oba", "오바댜", "옵"), ("jnh", "요나", "욘"), ("mic", "미가", "미"),
    ("nam", "나훔", "나"), ("hab", "하박국", "합"), ("zep", "스바냐", "습"),
    ("hag", "학개", "학"), ("zec", "스가랴", "슥"), ("mal", "말라기", "말"),
    ("mat", "마태복음", "마"), ("mrk", "마가복음", "막"), ("luk", "누가복음", "눅"),
    ("jhn", "요한복음", "요"), ("act", "사도행전", "행"), ("rom", "로마서", "롬"),
    ("1co", "고린도전서", "고전"), ("2co", "고린도후서", "고후"), ("gal", "갈라디아서", "갈"),
    ("eph", "에베소서", "엡"), ("php", "빌립보서", "빌"), ("col", "골로새서", "골"),
    ("1th", "데살로니가전서", "살전"), ("2th", "데살로니가후서", "살후"),
    ("1ti", "디모데전서", "딤전"), ("2ti", "디모데후서", "딤후"), ("tit", "디도서", "딛"),
    ("phm", "빌레몬서", "몬"), ("heb", "히브리서", "히"), ("jas", "야고보서", "약"),
    ("1pe", "베드로전서", "벧전"), ("2pe", "베드로후서", "벧후"), ("1jn", "요한일서", "요일"),
    ("2jn", "요한이서", "요이"), ("3jn", "요한삼서", "요삼"), ("jud", "유다서", "유"),
    ("rev", "요한계시록", "계"),
]
BOOK_CODES = frozenset(b[0] for b in _BOOKS)
NAME_TO_CODE: dict[str, str] = {}
for _code, _full, _abbr in _BOOKS:
    NAME_TO_CODE[_full] = _code
    NAME_TO_CODE[_abbr] = _code
assert len(_BOOKS) == 66 and len(BOOK_CODES) == 66


def resolve_book(name: str) -> str:
    """한글 정식명/약어 또는 bskorea 코드 -> 코드. 정확 일치만(부분 일치 추측 금지). 모르면 BibleFetchError."""
    key = re.sub(r"[\s.]", "", str(name)).strip()
    if key in NAME_TO_CODE:
        return NAME_TO_CODE[key]
    if key.lower() in BOOK_CODES:
        return key.lower()
    raise BibleFetchError(
        f"알 수 없는 책: {name!r} (코드표에 없음; 요나는 'jnh'/'요나'/'욘' — 'jon' 은 빈 페이지가 온다)")


def _http_get(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:  # 네트워크/HTTP 오류도 조용히 넘기지 않는다
        raise BibleFetchError(f"fetch 실패: {url} ({e})")


_NUM_SPAN = re.compile(
    r'<span class="number">(?:<a name=focus></a>)?\s*([0-9]+(?:[-,~][0-9]+)?)(?:&nbsp;|\s)*</span>')


def parse_chapter_html(page: str, book: str, chap: int) -> dict[int, str]:
    """bskorea 페이지 HTML -> {절번호: 본문}. 계약 위반이면 BibleFetchError. (네트워크 없음 — 단위 테스트 가능)"""
    if not page or not page.strip():
        raise BibleFetchError(f"빈 페이지: {book} {chap}")
    # 요청한 책/장과 응답이 일치하는지(차단·리다이렉트·잘못된 코드 방어)
    mb = re.search(r'initBook\("([^"]*)"\)', page)
    mc = re.search(r'initChap\("([^"]*)"\)', page)
    if not mb or not mc:
        raise BibleFetchError(f"bskorea 페이지 형식이 아님(initBook/initChap 없음): {book} {chap}")
    if mb.group(1) != book or mc.group(1) != str(chap):
        raise BibleFetchError(
            f"응답 책/장 불일치: 요청 {book} {chap} / 응답 {mb.group(1)} {mc.group(1)}")
    if "<b>개역개정</b>" not in page:
        raise BibleFetchError(f"개역개정(GAE) 본문 표지 없음: {book} {chap}")

    # 본문 영역: 개역개정 표지 이후만 (상단 메뉴/스크립트 배제)
    body = page.split("<b>개역개정</b>", 1)[1]
    # 각주 팝업 div, 각주 링크 제거
    body = re.sub(r"<div id='D_[^>]*>.*?</div>", "", body, flags=re.S)
    body = re.sub(r"<font size=2><a class=comment.*?</a></font>", "", body, flags=re.S)

    parts = _NUM_SPAN.split(body)
    # parts = [pre, num1, text1, num2, text2, ...]
    if len(parts) < 3:
        raise BibleFetchError(f"절이 하나도 없음(빈/차단 페이지): {book} {chap}")
    verses: dict[int, str] = {}
    order: list[int] = []
    for i in range(1, len(parts), 2):
        raw_num, seg = parts[i], parts[i + 1]
        if not raw_num.isdigit():
            raise BibleFetchError(f"합쳐진/범위 절 번호 {raw_num!r}: 자동 처리 불가 — 수동 확인 ({book} {chap})")
        n = int(raw_num)
        # 절 본문은 이 절의 </span>(절 래퍼 종료) 또는 <br 에서 끝난다. 그 뒤(소제목·</div>·<script>=JS 꼬리)는 버린다.
        cut = len(seg)
        for marker in ("</span>", "<br"):
            k = seg.find(marker)
            if k != -1:
                cut = min(cut, k)
        seg = seg[:cut]
        text = re.sub(r"<[^>]+>", "", seg)
        text = html_lib.unescape(text)
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            raise BibleFetchError(f"{book} {chap}:{n} 본문이 비어 있음")
        if re.search(r"function\s*\(|\$\(|document\.|<script|</div>|&nbsp;|initBook", text):
            raise BibleFetchError(f"{book} {chap}:{n} 에 사이트 JS/HTML 꼬리 흔적: {text[-80:]!r}")
        if n in verses:
            raise BibleFetchError(f"{book} {chap}: 절 {n} 중복")
        verses[n] = text
        order.append(n)

    expected = list(range(1, len(order) + 1))
    if order != expected:
        missing = sorted(set(range(1, max(order) + 1)) - set(order))
        raise BibleFetchError(
            f"{book} {chap}: 절 번호가 1..N 연속이 아님 — 얻은 {order} (누락 {missing})")
    return verses


def fetch_chapter(book: str, chap: int, cache_dir: str | None = None) -> dict[int, str]:
    """book: 코드 또는 한글명. 검증을 통과한 {절: 본문} 만 반환. sec 파라미터는 절대 쓰지 않는다."""
    code = resolve_book(book)
    chap = int(chap)
    if chap < 1:
        raise BibleFetchError(f"장 번호 오류: {chap}")
    cache_file = None
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
        cache_file = os.path.join(cache_dir, f"{code}_{chap}.json")
        if os.path.isfile(cache_file):
            try:
                cached = {int(k): v for k, v in json.load(open(cache_file, encoding="utf-8")).items()}
                if sorted(cached) == list(range(1, len(cached) + 1)) and all(cached.values()):
                    return cached
            except Exception:
                pass  # 손상 캐시는 무시하고 재fetch
    url = BASE_URL.format(book=code, chap=chap)
    assert "sec=" not in url
    verses = parse_chapter_html(_http_get(url), code, chap)
    if cache_file:
        json.dump(verses, open(cache_file, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return verses


_REF = re.compile(r"^\s*(.+?)\s*(\d+)\s*[:：]\s*(\d+)(?:\s*[-~–]\s*(\d+))?\s*$")


def parse_ref(ref: str):
    m = _REF.match(ref)
    if not m:
        raise BibleFetchError(f"참조 형식 오류: {ref!r} (예: '욘 4:11', '합 2:3-5')")
    book = resolve_book(m.group(1))
    chap, a = int(m.group(2)), int(m.group(3))
    b = int(m.group(4)) if m.group(4) else a
    if b < a:
        raise BibleFetchError(f"절 범위 역순: {ref!r}")
    return book, chap, a, b


def fetch_verses(ref: str, cache_dir: str | None = None) -> dict[int, str]:
    book, chap, a, b = parse_ref(ref)
    ch = fetch_chapter(book, chap, cache_dir)
    missing = [v for v in range(a, b + 1) if v not in ch]
    if missing:
        raise BibleFetchError(f"{ref}: 이 장에는 {missing} 절이 없음(장은 1..{max(ch)}절)")
    return {v: ch[v] for v in range(a, b + 1)}


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    as_json = "--json" in argv
    cache_dir = None
    if "--cache-dir" in argv:
        cache_dir = argv[argv.index("--cache-dir") + 1]
        args = [a for a in args if a != cache_dir]
    try:
        if len(args) == 1:
            out = fetch_verses(args[0], cache_dir)
            label = args[0]
        elif len(args) == 2 and args[1].isdigit():
            out = fetch_chapter(args[0], int(args[1]), cache_dir)
            label = f"{args[0]} {args[1]}"
        else:
            print(__doc__); return 2
    except BibleFetchError as e:
        print(f"❌ BibleFetchError: {e}", file=sys.stderr); return 1
    if as_json:
        print(json.dumps({str(k): v for k, v in out.items()}, ensure_ascii=False, indent=1))
    else:
        for k, v in out.items():
            print(f"{label.split(':')[0].strip()}:{k}  {v}" if ":" in label else f"{k}  {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
