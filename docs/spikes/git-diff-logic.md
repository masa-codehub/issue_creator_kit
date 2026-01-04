# [Spike] git diff によるマージ差分特定ロジックの検証

## 1. 目的
ADR-003 で定義された「仮想キュー（Virtual Queue）」の実行トリガーにおいて、`main` ブランチへのマージ（push）時に `reqs/tasks/archive/` ディレクトリに新しく追加されたファイルを正確に特定するための `git diff` コマンドを確定する。

## 2. 検証内容
### 2.1 検証シナリオ
1. `drafts/` ディレクトリにタスクファイルを作成。
2. `feature` ブランチでファイルを `drafts/` から `archive/` へ移動。
3. `main` ブランチ（検証用ブランチ）に `feature` ブランチを `--no-ff` でマージ。
4. マージコミットに対して各種 `git diff` コマンドを実行し、移動したファイルが「追加（A）」として検出されるかを確認。

### 2.2 検証したコマンド
1. `git diff HEAD^1 HEAD --name-status`
   - 結果: `R100` (Rename) として検出される。
   - 課題: リネーム検出が有効な場合、`--diff-filter=A` では検出できない。

2. `git diff HEAD^1 HEAD --name-status --no-renames --diff-filter=A -- reqs/tasks/archive/`
   - 結果: `A` (Added) として正しく検出される。
   - 考察: porcelain コマンドである `git diff` でも目的は達成可能。

3. `git diff-tree -r --no-commit-id --name-status --diff-filter=A HEAD^1 HEAD -- reqs/tasks/archive/`
   - 結果: 何も検出されない（リネームとして扱われているため）。

4. `git diff-tree -r --no-commit-id --name-status --diff-filter=A --no-renames HEAD^1 HEAD -- reqs/tasks/archive/`
   - 結果: `A` (Added) として正しく検出される。
   - 考察: plumbing コマンドである `git diff-tree` はスクリプトでの利用に適しており、より安定した動作が期待できるため、こちらを採用する。

## 3. 結論
以下のコマンドを使用することで、`drafts/` から `archive/` への移動を含め、新規に追加されたファイルを確実に特定できる。

```bash
git diff-tree -r --no-commit-id --name-status --diff-filter=A --no-renames <base_sha> <compare_sha> -- reqs/tasks/archive/
```

### オプション解説
- `-r`: サブディレクトリを再帰的に探索する。
- `--no-commit-id`: 出力からコミットIDを除外し、ファイルパスとステータスのみにする。
- `--name-status`: ファイル名とステータス（A, D, M等）を表示する。
- `--diff-filter=A`: **追加（Added）** されたファイルのみを抽出する。
- `--no-renames`: **リネーム検出を無効化** する。これにより、他ディレクトリからの移動（Rename）が「移動元での削除」と「移動先での追加」として分離され、`--diff-filter=A` で移動先のファイルをキャッチできるようになる。
- `-- reqs/tasks/archive/`: 指定したディレクトリ配下の変更のみを対象とする。

### GitHub Actions での利用イメージ
push イベントの場合、以下のように比較範囲を指定する。

```bash
git diff-tree -r --no-commit-id --name-status --diff-filter=A --no-renames ${{ github.event.before }} ${{ github.event.after }} -- reqs/tasks/archive/
```

## 4. 注意事項
- このコマンドは「ファイルの追加」を検知するものであり、そのファイルが「未採番（Issue 番号を持っていない）」かどうかの判定は、取得したファイルリストを元に ICK がファイル内容（Frontmatter 等）を確認して行う必要がある。
- マージコミットの場合、`<base_sha>` にはマージ先の親（通常は `HEAD^1`）を指定することで、マージによって持ち込まれた全変更を対象にできる。
