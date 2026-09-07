#!/usr/bin/env python3
"""build.py のテスト。実行: python3 test_build.py"""
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build


def test_号数の降順で並ぶ():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "issues.json"
        p.write_text(json.dumps([
            {"no": 1, "date": "2026-07-11", "headline": "あ", "pdf": "weekly-001.pdf"},
            {"no": 3, "date": "2026-07-25", "headline": "う", "pdf": "weekly-003.pdf"},
            {"no": 2, "date": "2026-07-18", "headline": "い", "pdf": "weekly-002.pdf"},
        ], ensure_ascii=False), encoding="utf-8")
        got = [i["no"] for i in build.load_issues(p)]
    assert got == [3, 2, 1], got


def test_見出しの記号がエスケープされる():
    out = build.render([
        {"no": 1, "date": "2026-07-11", "headline": "<script>x</script>",
         "pdf": "weekly-001.pdf"},
    ])
    assert "<script>" not in out, "生のタグが出力に残っている"
    assert "&lt;script&gt;" in out


def test_PDFへのリンクが相対パスで入る():
    out = build.render([
        {"no": 9, "date": "2026-09-05", "headline": "見出し", "pdf": "weekly-009.pdf"},
    ])
    assert 'href="pdf/weekly-009.pdf"' in out, out


def test_号数と発行日と見出しが表示される():
    out = build.render([
        {"no": 9, "date": "2026-09-05", "headline": "教員給与の改定", "pdf": "weekly-009.pdf"},
    ])
    for want in ("第9号", "2026-09-05", "教員給与の改定"):
        assert want in out, want


def test_1件もなくてもHTMLになる():
    out = build.render([])
    assert "<html" in out and "</html>" in out


def test_ファイルに書き出せる():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "issues.json").write_text(json.dumps([
            {"no": 1, "date": "2026-07-11", "headline": "あ", "pdf": "weekly-001.pdf"},
        ], ensure_ascii=False), encoding="utf-8")
        build.main(root)
        out = root / "weekly" / "index.html"
        assert out.exists(), "weekly/index.html が作られていない"
        assert "第1号" in out.read_text(encoding="utf-8")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
    print("すべて通った")
