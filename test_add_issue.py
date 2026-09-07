#!/usr/bin/env python3
"""add_issue.py のテスト。実行: python3 test_add_issue.py"""
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import add_issue


def _setup(d):
    """空の作業場を1つ作り、ダミーPDFのパスを返す。"""
    root = Path(d) / "site"
    root.mkdir()
    (root / "issues.json").write_text("[]", encoding="utf-8")
    src = Path(d) / "元のPDF 第9号.pdf"
    src.write_bytes(b"%PDF-1.4 dummy")
    return root, src


def test_ファイル名は号数3桁になる():
    assert add_issue.pdf_name(9) == "weekly-009.pdf"
    assert add_issue.pdf_name(123) == "weekly-123.pdf"


def test_同じ号を二度追加しても重複しない():
    issues = [{"no": 9, "date": "2026-09-05", "headline": "古い", "pdf": "weekly-009.pdf"}]
    got = add_issue.upsert(issues, {"no": 9, "date": "2026-09-05",
                                    "headline": "新しい", "pdf": "weekly-009.pdf"})
    assert len(got) == 1, got
    assert got[0]["headline"] == "新しい"


def test_あとから古い号を足しても降順に並ぶ():
    issues = [{"no": 9, "date": "2026-09-05", "headline": "九", "pdf": "weekly-009.pdf"}]
    got = add_issue.upsert(issues, {"no": 3, "date": "2026-07-25",
                                    "headline": "三", "pdf": "weekly-003.pdf"})
    assert [i["no"] for i in got] == [9, 3], got


def test_PDFがコピーされ一覧とページが更新される():
    with tempfile.TemporaryDirectory() as d:
        root, src = _setup(d)
        dst = add_issue.run(src, 9, "2026-09-05", "教員給与の改定", root=root)
        assert dst == root / "weekly" / "pdf" / "weekly-009.pdf"
        assert dst.exists(), "PDFがコピーされていない"
        data = json.loads((root / "issues.json").read_text(encoding="utf-8"))
        assert data[0]["no"] == 9 and data[0]["headline"] == "教員給与の改定"
        page = (root / "weekly" / "index.html").read_text(encoding="utf-8")
        assert "第9号" in page and "教員給与の改定" in page


def test_二度走らせても結果が変わらない():
    with tempfile.TemporaryDirectory() as d:
        root, src = _setup(d)
        add_issue.run(src, 9, "2026-09-05", "見出し", root=root)
        first = (root / "weekly" / "index.html").read_text(encoding="utf-8")
        add_issue.run(src, 9, "2026-09-05", "見出し", root=root)
        second = (root / "weekly" / "index.html").read_text(encoding="utf-8")
        assert first == second
        assert len(json.loads((root / "issues.json").read_text(encoding="utf-8"))) == 1


def test_日付の形が違えば止まる():
    with tempfile.TemporaryDirectory() as d:
        root, src = _setup(d)
        try:
            add_issue.run(src, 9, "2026/09/05", "見出し", root=root)
        except ValueError:
            return
        raise AssertionError("日付の形が違うのに通ってしまった")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
    print("すべて通った")
