#!/usr/bin/env python3
"""各ページのローカルリンク切れを見つける。実行: python3 test_links.py"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGES = [HERE / "index.html", HERE / "weekly" / "index.html"]

HREF = re.compile(r'(?:href|src)="([^"]+)"')


def local_targets(text):
    """外部URL・アンカー以外のリンク先を返す。"""
    out = []
    for h in HREF.findall(text):
        if h.startswith(("http://", "https://", "#", "mailto:", "data:")):
            continue
        out.append(h.split("#")[0].split("?")[0])
    return [h for h in out if h]


def test_ローカルリンクが全部存在する():
    missing = []
    for page in PAGES:
        assert page.exists(), "ページが無い: {}".format(page)
        for href in local_targets(page.read_text(encoding="utf-8")):
            target = (page.parent / href).resolve()
            if not target.exists():
                missing.append("{} -> {}".format(page.name, href))
    assert not missing, "リンク切れ: {}".format(missing)


def test_トップにバックナンバーとnoteへの導線がある():
    text = (HERE / "index.html").read_text(encoding="utf-8")
    assert 'href="weekly/"' in text, "バックナンバーへのリンクが無い"
    assert "https://note.com/nao_school" in text, "noteへのリンクが無い"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
    print("すべて通った")
