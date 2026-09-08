#!/usr/bin/env python3
"""issues.json から weekly/index.html を組み立てる。

実行: python3 build.py
weekly/index.html は毎回上書きされる。手で編集しないこと。
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>学校事務ウィークリー バックナンバー｜なお</title>
<meta name="description" content="全国の公立学校事務職員に向けて、週に1回まとめている紙面のバックナンバーです。">
<link rel="stylesheet" href="../style.css">
</head>
<body>

<header class="masthead wrap">
  <p class="tagline">週に一度、五分で追いつく。</p>
  <div class="who">
    <p class="back"><a href="../">← なおのページ</a></p>
    <h1>学校事務ウィークリー</h1>
    <p class="handle">全国の公立学校事務職員へ</p>
    <p class="intro">学校事務と教育まわりのニュースを、実務メモを付けて1枚にまとめています。
    新しい号が出たら、公式LINEでお知らせしています。</p>
  </div>
  <img class="mascot" src="../mascot-weekly.png" alt="">
</header>

<main class="sec wrap">
  <h2>バックナンバー</h2>
  <p class="note">見出しは各号のトップ記事です。PDFが開きます。</p>
  <ul class="issues">
{{ROWS}}
  </ul>
  <p class="count">全{{COUNT}}号</p>
</main>

<footer class="foot wrap">
  <p>編集: なお｜一人で抱え込まない学校事務</p>
</footer>

</body>
</html>
"""

ROW = """  <li class="issue">
    <a href="pdf/{pdf}">
      <span class="no">第{no}号</span>
      <span class="date">{date}</span>
      <span class="headline">{headline}</span>
    </a>
  </li>"""


def load_issues(path):
    """issues.json を読み、号数の降順で返す。"""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return sorted(data, key=lambda x: x["no"], reverse=True)


def render(issues):
    """号の一覧から HTML 文字列を作る。"""
    rows = "\n".join(
        ROW.format(
            pdf=html.escape(str(i["pdf"]), quote=True),
            no=int(i["no"]),
            date=html.escape(str(i["date"])),
            headline=html.escape(str(i["headline"])),
        )
        for i in issues
    )
    return TEMPLATE.replace("{{ROWS}}", rows).replace("{{COUNT}}", str(len(issues)))


def main(root=HERE):
    root = Path(root)
    issues = load_issues(root / "issues.json")
    out = root / "weekly" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(issues), encoding="utf-8")
    print("出力: {}（{}号）".format(out, len(issues)))


if __name__ == "__main__":
    main()
