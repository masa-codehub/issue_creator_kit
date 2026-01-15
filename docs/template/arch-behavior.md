# [Scenario Name] Sequence

## Scenario Overview
<!-- 
このシーケンス図が表現する物語（シナリオ）の概要を定義します。
- **Goal:** ユーザーまたはシステムが、このフローを通じて最終的に達成したいこと。
- **Trigger:** 処理を開始するイベント（HTTP Request, Cron Schedule, User Action, Message Receive）。
- **Type:** `[Sync (Real-time) | Async (Background) | Batch]` - 処理の性質。
-->

## Contracts (Pre/Post)
<!-- 契約条件（Contract）を定義し、振る舞いの厳密さを担保します。 -->
- **Pre-conditions (前提):**
  <!-- このフローが開始されるために満たされているべき条件（例：Userがログイン済み、在庫が存在する）。 -->
- **Post-conditions (保証):**
  <!-- フローが正常終了した時に、システムが保証する状態（例：決済レコードがCOMMITEDである、メール送信キューにタスクがある）。 -->

## Related Structures
<!-- 登場するコンポーネントの定義はここには書かず、Structure定義へのリンクを貼ります。 -->
*   `[Component Name]` (see `[link to structure doc]`)

## Diagram (Sequence)
```mermaid
sequenceDiagram
    autonumber
    %% ここにMermaid記法でシーケンス図を描画します。
    %% ParticipantA->>ParticipantB: Message (Sync)
    %% ParticipantB-->>ParticipantA: Response
    %% ParticipantA-)ParticipantC: Message (Async)
```

## Reliability & Failure Handling
<!-- Data-Intensive Reliability: 正常系だけでなく、異常系を厳密に定義します。 -->
- **Consistency Model:** `[ACID | Eventual Consistency | SAGA]`
  <!-- トランザクション管理の方針（強い整合性か、結果整合性か）。 -->
- **Failure Scenarios:**
  <!-- 各ステップで失敗した場合の挙動 -->
  - *Network Timeout:* `[API呼び出しがタイムアウトした場合の挙動（例: 3回リトライ後、503エラー）]`
  - *Worker Down:* `[処理中にプロセスが落ちた場合の挙動（例: メッセージはQueueに残り、復帰後に再開）]`
  - *Logic Error:* `[ビジネスロジックエラー時の挙動（例: 補償トランザクションを実行し、ステータスをFAILEDにする）]`
