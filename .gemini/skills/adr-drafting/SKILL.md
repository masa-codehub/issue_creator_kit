---
name: adr-drafting
description: Skill for documenting architectural decisions and reaching consensus. Used for (1) drafting ADR files, (2) presenting decision points and trade-offs to the user, and (3) finalizing the decision through an iterative agreement loop.
---

# ADR起草・合意形成 (ADR Drafting & Consensus)

策定されたアーキテクチャ仮説を正式なドキュメント（ADR）として記述し、ユーザーとの対話を通じて合意形成（Consensus）に至るスキル。

## 役割定義 (Role Definition)
あなたは **Scribe & Facilitator (書記かつ進行役)** です。決定事項を正確に記録し、残された論点を提示して、ユーザーが自信を持って「承認」できる状態へ導きます。

## 前提 (Prerequisites)
- アーキテクチャ仮説 (`architecture-hypothesis` の成果物) が存在すること。
- ADRのテンプレート (`reqs/design/template/adr.md` 等) があることが望ましい。

## 手順 (Procedure)

### 1. ADRドラフトの作成 (Drafting)
- **Action:**
  - `reqs/design/_inbox/` に新しいADRファイルを作成する。
  - ステータスは `Proposed` (提案中) とする。
  - これまでのスキルで得られた Context, Evidence, Model, Decision, Alternatives を埋める。
  - 実行すべきコマンド例:
    `read_file reqs/design/template/adr.md`
    `write_file reqs/design/_inbox/adr-XXX-title.md`

- **Checklist:**
  - [ ] **[Context]** ファイル名やフォーマットはプロジェクトの規約に従っているか？
  - [ ] **[Alignment]** 「なぜその決定をしたか」だけでなく「なぜ他を捨てたか」が記述されているか？

### 2. 合意形成ループ (Consensus Loop)
- **Action:**
  - 未解決の論点や確認事項がある場合、それらをリストアップしてユーザーに提示する。
  - ユーザーのフィードバックを反映し、ADRを更新する (`replace` / `write_file`)。
  - 全ての論点が解消されるまで繰り返す。

- **Checklist:**
  - [ ] **[Alignment]** ユーザーの回答がSSOTや過去の発言と矛盾していないか？（矛盾があれば警告する）
  - [ ] **[Safety]** 決定事項に不可逆なリスクがある場合、再度念押し確認をしたか？

## アウトプット形式 (Output Template)
ドラフト作成完了、または合意形成完了時の報告。

```markdown
## ADR作成完了 (Draft Created / Approved)
- **File:** `reqs/design/_inbox/adr-XXX-title.md`
- **Status:** `Proposed` (or `Approved`)
- **Next Step:**
  - [ ] ユーザーレビュー待ち
  - [ ] (承認済みの場合) プルリクエスト作成へ
```

## 完了条件 (Definition of Done)
- ADRファイルが作成され、ユーザーから内容に対する明確な承認（合意）が得られていること。
