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
    assert "<script>x</script>" not in out, "生のタグが出力に残っている"
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


def test_LINE登録への導線が一覧の前後にある():
    out = build.render([
        {"no": 9, "date": "2026-09-05", "headline": "見出し", "pdf": "weekly-009.pdf"},
    ])
    assert out.count('href="https://lin.ee/O8516km"') == 2, "LINE登録のリンクが2か所にない"
    top = out.index("lin.ee/O8516km")
    last = out.rindex("lin.ee/O8516km")
    issues = out.index('class="issues"')
    assert top < issues < last, "一覧の前と後ろに置かれていない"


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


MARKS = "".join(
    "<!-- {0}:ここから（build.py が書き換える。手で編集しない） -->\n古い\n<!-- {0}:ここまで -->\n".format(n)
    for n in ("目次", "ウィークリー最新号", "つくったもの"))

WORK = {"title": "t", "desc": "d", "url": "u/", "img": "img/x.webp", "cta": "くわしく"}


def test_最新号は先頭の号で日付が年月日になる():
    out = build.render_latest([
        {"no": 14, "date": "2026-10-10", "headline": "見出し<b>", "pdf": "weekly-014.pdf"},
        {"no": 13, "date": "2026-10-03", "headline": "前の号", "pdf": "weekly-013.pdf"},
    ])
    assert "第14号" in out and "2026年10月10日" in out, out
    assert 'href="weekly/pdf/weekly-014.pdf"' in out, out
    assert "&lt;b&gt;" in out and "<b>" not in out
    assert "前の号" not in out


def test_号がなければ最新号は空():
    assert build.render_latest([]) == ""


def test_つくったものはファイル順でエスケープされる():
    out = build.render_works([
        {"title": "A&B", "desc": "説明", "url": "kasuhara/", "img": "img/card-a.webp", "cta": "ひらく"},
        {"title": "二番", "desc": "", "url": "https://example.com/", "img": "img/card-b.webp", "cta": "くわしく"},
    ])
    assert out.index("A&amp;B") < out.index("二番")
    assert 'id="works"' in out and 'href="kasuhara/"' in out
    assert 'src="img/card-a.webp"' in out


def test_つくったものが空なら区切りごと出ない():
    assert build.render_works([]) == ""


def test_つくったものに販売の言葉が出ない():
    out = build.render_works([WORK])
    for ng in ("販売", "購入", "円"):
        assert ng not in out, ng


def test_目次はつくったものの有無で変わる():
    with_works = build.render_toc(True)
    assert 'href="#works"' in with_works
    assert 'href="#works"' not in build.render_toc(False)
    for a in ("#weekly", "#fields", "#teachers"):
        assert a in with_works, a


def test_目印の間だけ書き換わり二度やっても同じ():
    s = "前\n" + MARKS + "後"
    once = build.replace_block(s, "目次", "新しい")
    assert once.startswith("前\n") and once.endswith("後")
    assert "新しい" in once and once.count("古い") == 2
    assert build.replace_block(once, "目次", "新しい") == once


def test_目印がなければ止まる():
    try:
        build.replace_block("目印なし", "目次", "x")
    except ValueError as e:
        assert "目次" in str(e)
        return
    assert False, "ValueError にならない"


def test_worksも号もなくてもトップが組める():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "issues.json").write_text("[]", encoding="utf-8")
        (root / "index.html").write_text("<html>\n" + MARKS + "</html>", encoding="utf-8")
        build.main(root)
        top = (root / "index.html").read_text(encoding="utf-8")
        assert 'id="works"' not in top and "古い" not in top
        assert top.startswith("<html>") and top.endswith("</html>")


def test_トップに最新号とつくったものが入る():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "issues.json").write_text(json.dumps([
            {"no": 2, "date": "2026-07-18", "headline": "二号の見出し", "pdf": "weekly-002.pdf"},
        ], ensure_ascii=False), encoding="utf-8")
        (root / "works.json").write_text(json.dumps([WORK], ensure_ascii=False), encoding="utf-8")
        (root / "index.html").write_text("<html>\n" + MARKS + "</html>", encoding="utf-8")
        build.main(root)
        build.main(root)  # 二度目で崩れない
        top = (root / "index.html").read_text(encoding="utf-8")
        assert "二号の見出し" in top and 'id="works"' in top and 'href="#works"' in top
        assert top.count('id="works"') == 1


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
    print("すべて通った")
