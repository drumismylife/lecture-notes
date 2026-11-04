#!/usr/bin/env python3
"""bible_fetch.py 오프라인 단위 테스트 (네트워크 없음). 실행: python3 scripts/test_bible_fetch.py"""
import re, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bible_fetch as bf

def page(book="hab", chap=2, verses=None, focus=None, title=True):
    """합성 bskorea 페이지 (실제 구조 모사)."""
    verses = verses if verses is not None else {1: "첫째 절", 2: "둘째 절", 3: "셋째 절"}
    h = f'<html><script>initBook("{book}"); initChap("{chap}");</script><b>개역개정</b><br/><font class="chapNum">제 {chap} 장</font><br />'
    for n, t in verses.items():
        anchor = "<a name=focus></a>" if n == focus else ""
        h += f'<span><span class="number">{anchor}{n}&nbsp;&nbsp;&nbsp;</span>{t}</font></span><br />'
    if title:
        h += '<div style="x"></div><script>$(function(){ document.all.x; });</script></div></body></html>'
    return h

class T(unittest.TestCase):
    def test_pass_contiguous(self):
        self.assertEqual(bf.parse_chapter_html(page(), "hab", 2), {1: "첫째 절", 2: "둘째 절", 3: "셋째 절"})
    def test_pass_focus_anchor_every_verse(self):
        for f in (1, 2, 3):
            self.assertEqual(len(bf.parse_chapter_html(page(focus=f), "hab", 2)), 3)
    def test_js_tail_stripped_from_last_verse(self):
        self.assertEqual(bf.parse_chapter_html(page(), "hab", 2)[3], "셋째 절")
    def test_reject_missing_verse(self):
        with self.assertRaises(bf.BibleFetchError): bf.parse_chapter_html(page(verses={1: "a", 2: "b", 4: "d"}), "hab", 2)
    def test_reject_not_starting_at_1(self):
        with self.assertRaises(bf.BibleFetchError): bf.parse_chapter_html(page(verses={2: "b", 3: "c"}), "hab", 2)
    def test_reject_duplicate(self):
        with self.assertRaises(bf.BibleFetchError): bf.parse_chapter_html(page().replace("셋째", "둘째").replace(">3&nbsp", ">2&nbsp"), "hab", 2)
    def test_reject_empty_page(self):
        for p in ("", "   ", page(verses={})):
            with self.assertRaises(bf.BibleFetchError): bf.parse_chapter_html(p, "hab", 2)
    def test_reject_wrong_book_or_chapter_in_response(self):
        with self.assertRaises(bf.BibleFetchError): bf.parse_chapter_html(page(book="jnh"), "hab", 2)
        with self.assertRaises(bf.BibleFetchError): bf.parse_chapter_html(page(chap=3), "hab", 2)
    def test_reject_not_bskorea_page(self):
        with self.assertRaises(bf.BibleFetchError): bf.parse_chapter_html("<html>403 Forbidden</html>", "hab", 2)
    def test_reject_empty_verse_text(self):
        with self.assertRaises(bf.BibleFetchError): bf.parse_chapter_html(page(verses={1: "a", 2: " "}), "hab", 2)
    def test_merged_marker_ok_and_reported(self):
        pg = page(verses={1: "a", 2: "b", 3: "c"}).replace(">3&nbsp;", ">3-4&nbsp;")
        m = []; v = bf.parse_chapter_html(pg, "hab", 2, m)
        self.assertEqual(sorted(v), [1, 2, 3, 4]); self.assertEqual(v[3], v[4]); self.assertEqual(m, [(3, 4)])
    def test_reject_merged_gap_or_reversed(self):
        for pg in (page(verses={1: "a", 2: "b", 3: "c"}).replace(">2&nbsp;", ">2-3&nbsp;"),   # 2-3 then 3 => duplicate
                   page(verses={1: "a", 2: "b"}).replace(">2&nbsp;", ">4-3&nbsp;"),             # reversed
                   page(verses={1: "a", 2: "b", 3: "c"}).replace(">3&nbsp;", ">5-6&nbsp;")):   # gap (1,2,5,6)
            with self.assertRaises(bf.BibleFetchError): bf.parse_chapter_html(pg, "hab", 2)
    def test_unknown_book(self):
        for bad in ("jon", "xyz", "요나서", "", "요나나"):
            with self.assertRaises(bf.BibleFetchError, msg=bad): bf.resolve_book(bad)
    def test_book_table(self):
        self.assertEqual(bf.resolve_book("욘"), "jnh"); self.assertEqual(bf.resolve_book("요나"), "jnh")
        self.assertEqual(bf.resolve_book("요"), "jhn"); self.assertEqual(bf.resolve_book("합"), "hab")
        self.assertEqual(bf.resolve_book("JNH"), "jnh"); self.assertEqual(len(bf.BOOK_CODES), 66)
    def test_ref_parse(self):
        self.assertEqual(bf.parse_ref("욘 4:11"), ("jnh", 4, 11, 11)); self.assertEqual(bf.parse_ref("합 2:3-5"), ("hab", 2, 3, 5))
        for bad in ("욘 4", "욘 4:5-3", "foo 1:1"):
            with self.assertRaises(bf.BibleFetchError): bf.parse_ref(bad)
    def test_url_never_has_sec(self):
        self.assertNotIn("sec=", bf.BASE_URL)

if __name__ == "__main__":
    unittest.main(verbosity=1)
