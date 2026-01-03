---
title: "GitHub API によるブランチ・PR操作の実現可能性調査"
labels: ["task", "P1", "BACKENDCODER"]
roadmap: "reqs/roadmap/_inbox/roadmap-adr003-task-lifecycle.md"
task_id: "T1-2"
depends_on: ["issue-T1-1.md"]
status: "Draft"
---
# {{title}}

## 1. 目的と背景
- **As-is**: ICK は現在 Issue 作成のみを行っており、ブランチ作成や PR 作成の API 実装経験がない。
- **To-be**: フェーズ連鎖に必要な「ブランチ作成」と「PR作成」が GitHub REST API で実行可能であることを確認し、必要な権限（Scope）を特定する。

## 2. 実装手順
- [ ] `curl` または `requests` を用いた Spike スクリプトで、テスト用リポジトリに対して PR を作成できるか検証する。
- [ ] 必要なパラメータ（head, base, title, body）の最小構成を確認。

## 6. 成果物
- 調査結果を Issue コメントに記録。
