#!/usr/bin/env python3
"""noteの記事数を取ってきて、index.html の「書いていること」を書き直す。

実行: python3 fetch_fields.py

記事が増えたら、これを走らせて index.html をコミットする。
数字を手で書き写さないこと（一度それで間違えた。36本と書いたが実際は72本だった）。

noteのAPIは1ページ6件しか返さない。isLastPage が真になるまでページを繰る。
"""
import json
import re
import sys
import time
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
CREATOR = "nao_school"
API = "https://note.com/api/v2/creators/{}/contents?kind=note&page={}"

# 領域として扱わないもの。記事の総数には数えるが、タブには出さない。
NOT_A_FIELD = {"領域の表記なし", "シリーズ外"}

START = "<!-- 書いていること:ここから（fetch_fields.py が書き換える。手で編集しない） -->"
END = "<!-- 書いていること:ここまで -->"


def fetch_all(creator=CREATOR, sleep=0.2):
    """全記事の (タイトル, キー) を返す。APIの totalCount も返す。"""
    titles = []
    total = None
    page = 1
    while True:
        with urllib.request.urlopen(API.format(creator, page)) as r:
            d = json.load(r)["data"]
        total = d.get("totalCount")
        for n in d.get("contents", []):
            titles.append(n.get("name", ""))
        if d.get("isLastPage"):
            break
        page += 1
        if page > 100:
            raise RuntimeError("ページが100を超えた。APIの形が変わった可能性がある")
        time.sleep(sleep)
    return titles, total


def count_fields(titles):
    """タイトルの「実務編（◯◯）」から領域を数える。"""
    c = Counter()
    for t in titles:
        m = re.search(r"実務編（([^）]+)）", t)
        if m:
            c[m.group(1)] += 1
        elif "思考整理" in t:
            c["領域の表記なし"] += 1
        else:
            c["シリーズ外"] += 1
    return c


def weight(n):
    """タブの濃さ。本数の多さをそのまま見た目にする。"""
    if n >= 6:
        return 3
    if n >= 2:
        return 2
    return 1


def render(counts, total):
    fields = [(f, n) for f, n in counts.most_common() if f not in NOT_A_FIELD]
    rows = "\n".join(
        '      <li data-weight="{w}"><span>{f}</span><span class="n">{n}</span></li>'.format(
            w=weight(n), f=f, n=n)
        for f, n in fields
    )
    return (
        '    <p class="note">noteに{total}本。実務の領域ごとに整理しています。数字は本数です。</p>\n'
        '    <ul class="tabs">\n{rows}\n    </ul>'
    ).format(total=total, rows=rows)


def main():
    titles, total = fetch_all()
    if len(titles) != total:
        print("取得件数({})とAPIのtotalCount({})が食い違う。中断する。".format(len(titles), total))
        return 1
    counts = count_fields(titles)
    block = render(counts, total)

    path = HERE / "index.html"
    s = path.read_text(encoding="utf-8")
    if START not in s or END not in s:
        print("index.html に目印が見つからない。中断する。")
        return 1
    head, rest = s.split(START, 1)
    _, tail = rest.split(END, 1)
    path.write_text(head + START + "\n" + block + "\n    " + END + tail, encoding="utf-8")

    print("記事 {}本 / 領域 {}種を書き込んだ".format(
        total, len([f for f in counts if f not in NOT_A_FIELD])))
    for f, n in counts.most_common():
        mark = "  " if f not in NOT_A_FIELD else "（タブに出さない）"
        print("  {:<16} {:>3}  {}".format(f, n, mark))
    return 0


if __name__ == "__main__":
    sys.exit(main())
