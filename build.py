#!/usr/bin/env python3
"""issues.json から weekly/index.html を組み立てる。

実行: python3 build.py
weekly/index.html は毎回上書きされる。手で編集しないこと。
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

# 公式LINE「なお」の友だち追加URL。note記事の末尾と同じもの。
LINE_URL = "https://lin.ee/O8516km"

TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>学校事務ウィークリー バックナンバー｜なお</title>
<meta name="description" content="全国の公立学校事務職員に向けて、週に1回まとめている紙面のバックナンバーです。">
<meta name="theme-color" content="#7f679a">
<meta property="og:type" content="website">
<meta property="og:title" content="学校事務ウィークリー バックナンバー｜なお">
<meta property="og:description" content="週に一度、五分で追いつく。学校事務と教育まわりのニュースを、実務メモ付きで1枚に。">
<meta property="og:url" content="https://tsj-coder.github.io/nao/weekly/">
<meta property="og:image" content="https://tsj-coder.github.io/nao/img/ogp.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="../img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Old+Mincho:wght@600&amp;display=swap">
<link rel="stylesheet" href="../style.css">
<script>
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('motion');
    setTimeout(function () { if (!window.gsap) document.documentElement.classList.remove('motion'); }, 2500);
  }
</script>
</head>
<body class="page-weekly">

<header class="hero hero-sub">
  <div class="wrap hero-in">
    <p class="hero-back"><a href="../">← なおのページ</a></p>
    <p class="hero-en">Weekly back numbers</p>
    <p class="hero-tag"><span>週に一度、</span><span>五分で追いつく。</span></p>
    <div class="hero-art" aria-hidden="true">
      <svg class="blob" viewBox="0 0 400 320">
        <path class="blob-a" d="M62 70 C128 6 262 14 318 66 C382 128 360 238 286 276 C210 314 92 304 50 240 C8 176 12 116 62 70 Z"/>
        <path class="blob-b" d="M96 92 C160 48 254 58 296 100 C338 150 318 222 254 252 C190 282 106 266 78 210 C52 158 54 120 96 92 Z"/>
      </svg>
      <img class="prop prop-1" src="../img/prop-papers.webp" alt="">
      <img class="prop prop-2" src="../img/prop-envelope.webp" alt="">
      <img class="hero-adult" src="../img/adult-hand.webp" alt="">
    </div>
    <div class="hero-name-box">
      <h1 class="hero-name">学校事務ウィークリー</h1>
      <p class="hero-handle">全国の公立学校事務職員へ。学校事務と教育まわりのニュースを、実務メモを付けて1枚にまとめています。</p>
    </div>
  </div>
</header>

<main>
  <section class="sec sec-tint" aria-label="公式LINEの友だち追加">
    <svg class="wave" viewBox="0 0 1200 60" preserveAspectRatio="none" aria-hidden="true"><path d="M0 34 C200 4 380 58 600 30 C800 6 1000 20 1200 34 L1200 60 L0 60 Z"/></svg>
    <div class="wrap sec-in">
      <div class="line-cta reveal">
        <p class="line-lead">最新号は、公式LINEで届きます</p>
        <p class="line-desc">毎週末、新しい号が出たらすぐにLINEでお届けします。このページを探しに来なくても、手元で読めます。</p>
        <a class="btn" href="{{LINE}}">LINEで友だち追加する</a>
      </div>
    </div>
  </section>

  <section class="sec" aria-labelledby="back-h">
    <svg class="wave" viewBox="0 0 1200 60" preserveAspectRatio="none" aria-hidden="true"><path d="M0 34 C200 4 380 58 600 30 C800 6 1000 20 1200 34 L1200 60 L0 60 Z"/></svg>
    <div class="wrap sec-in">
      <p class="eyebrow">Back numbers</p>
      <h2 id="back-h">バックナンバー</h2>
      <p class="lead">見出しは各号のトップ記事です。PDFが開きます。</p>
      <ul class="issues">
{{ROWS}}
      </ul>
      <p class="count">全{{COUNT}}号</p>
      <p class="line-again">次の号を見逃さないように。<a href="{{LINE}}">公式LINEで受け取る</a></p>
    </div>
  </section>
</main>

<footer class="foot">
  <div class="wrap">
    <p>編集: なお｜一人で抱え込まない学校事務</p>
  </div>
</footer>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/gsap.min.js" integrity="sha512-NcZdtrT77bJr4STcmsGAESr06BYGE8woZdSdEgqnpyqac7sugNO+Tr4bGwGF3MsnEkGKhU2KL2xh6Ec+BqsaHA==" crossorigin="anonymous" referrerpolicy="no-referrer" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/ScrollTrigger.min.js" integrity="sha512-P2IDYZfqSwjcSjX0BKeNhwRUH8zRPGlgcWl5n6gBLzdi4Y5/0O4zaXrtO4K9TZK6Hn1BenYpKowuCavNandERg==" crossorigin="anonymous" referrerpolicy="no-referrer" defer></script>
<script src="../motion.js" defer></script>
</body>
</html>
"""

ROW = """        <li class="issue reveal">
    <a href="pdf/{pdf}">
      <span class="no">第{no}号</span>
      <span class="date">{date}</span>
      <span class="headline">{headline}</span>
    </a>
  </li>"""


# ── トップページの、目印で挟んだ部分 ─────────────────
# index.html の目印の間だけを書き換える。外側（名乗り・先生方へ）は手で直せる。
MARK_START = "<!-- {}:ここから（build.py が書き換える。手で編集しない） -->"
MARK_END = "<!-- {}:ここまで -->"

# 区切りの上端の波。index.html の各区切りと同じ形にそろえる。
WAVE = ('<svg class="wave" viewBox="0 0 1200 60" preserveAspectRatio="none" aria-hidden="true">'
        '<path d="M0 34 C200 4 380 58 600 30 C800 6 1000 20 1200 34 L1200 60 L0 60 Z"/></svg>')

LATEST = """      <a class="latest reveal" href="weekly/pdf/{pdf}">
        <span class="latest-tag">最新号</span>
        <span class="latest-meta"><span class="latest-no">第{no}号</span><span class="latest-date">{date}</span></span>
        <span class="latest-head">{headline}</span>
        <span class="latest-go">PDFをひらく →</span>
      </a>"""

WORK = """        <li class="work reveal">
          <a href="{url}">
            <span class="work-art"><img src="{img}" alt="" loading="lazy"></span>
            <span class="work-body">
              <span class="work-title">{title}</span>
              <span class="work-desc">{desc}</span>
              <span class="work-cta">{cta} →</span>
            </span>
          </a>
        </li>"""

# 値段や「販売」の語は出さない（設計書3章）。有料かどうかは飛んだ先で分かればよい。
WORKS_SECTION = """  <section class="sec sec-tint" id="works" aria-labelledby="works-h">
    """ + WAVE + """
    <div class="wrap sec-in">
      <img class="sec-art" src="img/adult-board.webp" alt="">
      <p class="eyebrow">Works</p>
      <h2 id="works-h">つくったもの</h2>
      <p class="lead">現場で使っている道具と、ペンギンのスタンプ。</p>
      <ul class="works">
{{CARDS}}
      </ul>
      <img class="peek" src="img/kid-done.webp" alt="">
    </div>
  </section>"""

TOC_ITEMS = [("weekly", "ウィークリー"), ("fields", "書いていること"),
             ("works", "つくったもの"), ("teachers", "先生方へ")]


def esc(v):
    return html.escape(str(v), quote=True)


def replace_block(text, name, block):
    """目印「name」の間を block に置き換える。目印がなければ ValueError。"""
    start, end = MARK_START.format(name), MARK_END.format(name)
    if start not in text or end not in text:
        raise ValueError("index.html に目印「{}」が見つからない".format(name))
    head, rest = text.split(start, 1)
    _, tail = rest.split(end, 1)
    body = "\n" + block.rstrip("\n") + "\n" if block else "\n"
    return head + start + body + end + tail


def jdate(s):
    """2026-10-10 → 2026年10月10日"""
    y, m, d = (int(x) for x in str(s).split("-"))
    return "{}年{}月{}日".format(y, m, d)


def render_latest(issues):
    """号数の降順に並んだ一覧の先頭を、最新号の枠にする。号がなければ空。"""
    if not issues:
        return ""
    i = issues[0]
    return LATEST.format(pdf=esc(i["pdf"]), no=int(i["no"]),
                         date=esc(jdate(i["date"])), headline=esc(i["headline"]))


def load_works(path):
    """works.json を読む。無ければ空の一覧。"""
    p = Path(path)
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))


def render_works(works):
    """つくったものの区切りを丸ごと作る。1件もなければ区切りごと出さない。"""
    if not works:
        return ""
    cards = "\n".join(
        WORK.format(**{k: esc(w.get(k, "")) for k in ("title", "desc", "url", "img", "cta")})
        for w in works)
    return WORKS_SECTION.replace("{{CARDS}}", cards)


def render_toc(has_works):
    """目次のボタン。つくったものが無ければ、そのボタンも出さない。"""
    lis = "\n".join(
        '      <li><a href="#{}">{}</a></li>'.format(a, t)
        for a, t in TOC_ITEMS if has_works or a != "works")
    return '    <ul class="toc-list">\n{}\n    </ul>'.format(lis)


def update_top(root):
    """index.html の目次・最新号・つくったものを書き直す。"""
    root = Path(root)
    path = root / "index.html"
    s = path.read_text(encoding="utf-8")
    issues = load_issues(root / "issues.json")
    works = load_works(root / "works.json")
    s = replace_block(s, "目次", render_toc(bool(works)))
    s = replace_block(s, "ウィークリー最新号", render_latest(issues))
    s = replace_block(s, "つくったもの", render_works(works))
    path.write_text(s, encoding="utf-8")


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
    return (TEMPLATE.replace("{{ROWS}}", rows)
            .replace("{{COUNT}}", str(len(issues)))
            .replace("{{LINE}}", LINE_URL))


def main(root=HERE):
    root = Path(root)
    issues = load_issues(root / "issues.json")
    out = root / "weekly" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(issues), encoding="utf-8")
    print("出力: {}（{}号）".format(out, len(issues)))
    if (root / "index.html").exists():
        update_top(root)
        print("出力: {}（目次・最新号・つくったもの）".format(root / "index.html"))


if __name__ == "__main__":
    main()
