#!/usr/bin/env python3
"""今週号をアーカイブに追加する。

使い方:
    python3 add_issue.py <PDFのパス> <号数> <発行日 YYYY-MM-DD> "<トップ記事の見出し>"

例:
    python3 add_issue.py ~/Downloads/学校事務ウィークリー_第9号.pdf 9 2026-09-05 "教員給与の改定"

同じ号数を二度足しても重複しない（あとの内容で上書きされる）。
"""
import datetime
import json
import shutil
import sys
from pathlib import Path

import build

HERE = Path(__file__).resolve().parent


def pdf_name(no):
    """号数から、リポジトリに置くときのファイル名を作る。"""
    return "weekly-{:03d}.pdf".format(int(no))


def upsert(issues, entry):
    """同じ号数があれば置き換えて、号数の降順で返す。"""
    kept = [i for i in issues if int(i["no"]) != int(entry["no"])]
    kept.append(entry)
    return sorted(kept, key=lambda x: int(x["no"]), reverse=True)


def run(pdf_src, no, date, headline, root=HERE):
    """PDFをコピーし、一覧に足し、ページを組み直す。コピー先を返す。"""
    root = Path(root)
    pdf_src = Path(pdf_src)
    if not pdf_src.exists():
        raise FileNotFoundError("PDFが見つからない: {}".format(pdf_src))
    datetime.datetime.strptime(date, "%Y-%m-%d")  # 形が違えば ValueError

    dst_dir = root / "weekly" / "pdf"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / pdf_name(no)
    shutil.copyfile(pdf_src, dst)

    issues_path = root / "issues.json"
    issues = json.loads(issues_path.read_text(encoding="utf-8")) if issues_path.exists() else []
    issues = upsert(issues, {
        "no": int(no), "date": date, "headline": headline, "pdf": pdf_name(no),
    })
    issues_path.write_text(
        json.dumps(issues, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    build.main(root)
    return dst


def main(argv):
    if len(argv) != 5:
        print(__doc__)
        return 1
    dst = run(argv[1], argv[2], argv[3], argv[4])
    print("追加: {}".format(dst))
    print("この後: git add -A && git commit && git push")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
