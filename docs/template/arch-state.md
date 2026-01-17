# [Object Name] Lifecycle

## Subject Definition
<!-- 
状態遷移図の対象となるオブジェクトを定義します。
- **Target Object:** 状態を持つドメインオブジェクト（Entity）の名前。
- **Persistence:** `[DB Table Name | Redis Key | In-Memory]` - 状態がどこに保存されるか。
- **Concurrency Strategy:** `[Optimistic Locking (Version) | Pessimistic Locking | None]` - 同時更新時の排他制御戦略。
-->

## Diagram (State)
```mermaid
stateDiagram-v2
    %% ここにMermaid記法でステートマシン図を描画します。
    %% [*] --> State1
    %% State1 --> State2 : Event/Trigger
    %% State2 --> [*]
```

## State Definitions & Transitions
<!-- 各ステータスの意味と遷移ルールを表形式で定義します。 -->

| State | Definition | Trigger (Transition) | Side Effects |
| :--- | :--- | :--- | :--- |
| `[STATE_NAME]` | この状態が意味すること（ビジネス的な定義）。 | この状態へ遷移するトリガー（メソッド呼び出し、イベント受信）。 | 遷移時に発生する副作用（メール送信、ログ出力、他Entityの更新）。 |

## Invariants (不変条件)
<!-- 全ステータスを通じて、常に真でなければならない絶対的なビジネスルール。 -->
*   *e.g. 完了した注文の金額は、いかなるステータス変更でも変更されてはならない。*
*   *e.g. 削除フラグが立ったユーザーは、ログイン状態にはなれない。*
