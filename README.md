# nao

公式LINE「なお」の入口ページと、学校事務ウィークリーのバックナンバー。

- トップ: https://tsj-coder.github.io/nao/
- バックナンバー: https://tsj-coder.github.io/nao/weekly/

## 毎週やること

Claude Code に「今週号をアーカイブに追加して」と伝える。中で動くのは次の1行。

    python3 add_issue.py <PDFのパス> <号数> <発行日> "<トップ記事の見出し>"

PDFのコピー・issues.json への追記・weekly/index.html の組み直しが一度に走る。

## 入れてはいけないもの

**候補一覧メモ（採用・不採用の理由を書いたメモ）を、このリポジトリに入れない。**
gitは一度入れたファイルを消しても履歴に残る。候補一覧には選定の判断や、
勤務地が推測できる材料が入り得る。メモはGoogle Driveに置いたままにする。

## ファイルの役割

- `issues.json` … 号の一覧データ。毎週ここに1件増える
- `build.py` … issues.json から weekly/index.html を組み立てる
- `add_issue.py` … 毎週の追加作業をまとめて行う
- `weekly/index.html` … **手で編集しない。** build.py の出力
