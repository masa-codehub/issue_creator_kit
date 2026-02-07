# Goal Definition: ADR-008 Domain Models Specification

## 1. 達成目標 (Outcome)
ADR-008「Scanner Foundation」の核となるドメインモデルとガードレールの詳細仕様書を策定する。これにより、実装者が TDD サイクルを円滑に回せる状態にする。

## 2. 成果物 (Deliverables)
- `docs/specs/data/domain_models_adr008.md`: Task, ADR, TaskID, ADRID のデータ構造と制約の定義。
- `docs/specs/logic/graph_and_validators.md`: グラフ構造、循環参照検知、バリデーションロジックの定義。

## 3. 実装のステップ (Implementation Steps)
1. **Model Specification**: `domain_models_adr008.md` を作成し、Pydantic モデルの各フィールド、型、Regex 制約を定義する。
2. **Logic Specification**: `graph_and_validators.md` を作成し、`TaskNode`, `TaskGraph` の振る舞いと、エラーハンドリング（`CYCLE_DETECTED` 等）の詳細を定義する。
3. **Verify Criteria**: 各仕様書に、Happy Path と Error Path のテストケース（入力と期待される結果）を記述する。
4. **Consistency Audit**: 既存の `definitions.md` および `arch-structure-008-scanner.md` との整合性を確認する。

## 4. 検証方法 (Definition of Done)
- [ ] 指定されたパスに 2 つの仕様書が作成されていること。
- [ ] 各仕様書に「TDD 検証基準 (Verify Criteria)」が含まれていること。
- [ ] 曖昧な表現（TBD, 等）が排除されていること。
- [ ] 自己監査（auditing-ssot）をパスしていること。

### 検証コマンド
```bash
ls docs/specs/data/domain_models_adr008.md
ls docs/specs/logic/graph_and_validators.md
grep -E "TBD|Pending|Any" docs/specs/data/domain_models_adr008.md docs/specs/logic/graph_and_validators.md || echo "No ambiguity found"
```
