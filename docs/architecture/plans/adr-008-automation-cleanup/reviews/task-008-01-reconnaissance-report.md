# Reconnaissance Report - Archive Obsolete Architecture Docs

## 1. 調査対象 (Scope)
- **Target Files:**
    - `docs/architecture/arch-behavior-003-autopr.md`
    - `docs/architecture/arch-behavior-003-creation.md`
    - `docs/architecture/arch-state-003-task-lifecycle.md`
    - `docs/architecture/arch-structure-003-vqueue.md`
- **Destination:** `docs/architecture/archive/`
- **Branch:** `feature/task-008-01-archive-docs`

## 2. 収集された事実 (Gathered Facts)
- **File Status:**
    - すべての対象ファイルは既に `docs/architecture/archive/` に `git mv` され、ステージングされている。
    - `arch-behavior-003-autopr.md` と `arch-behavior-003-creation.md` はステージング後に修正（modified）されている。
    - `arch-state-003-task-lifecycle.md` と `arch-structure-003-vqueue.md` はステージング後に修正されていない。
- **Content Verification:**
    - 4ファイルすべてに「DEPRECATED」の警告が追加されている。
    - `arch-behavior-003-autopr.md` と `arch-behavior-003-creation.md` では、リンクのパスが `../` を含む形式に修正されている。
    - `arch-state-003-task-lifecycle.md` と `arch-structure-003-vqueue.md` では、リンクのパスが古いまま（root相対のつもりでカレント相対になっている）である可能性がある。
- **Directory Verification:**
    - `docs/architecture/archive/` ディレクトリは既に存在し、ファイルが格納されている。

## 3. 証拠 (Evidence)
- `git status` output confirms renames are staged.
- `read_file` confirms DEPRECATED notice presence.
- `git diff` shows path adjustments in 2 out of 4 files.

## 4. 懸念事項 (Concerns)
- 残りの2ファイル (`arch-state-003-task-lifecycle.md`, `arch-structure-003-vqueue.md`) の内部リンクが壊れている可能性がある（移動に伴う相対パスの不整合）。
