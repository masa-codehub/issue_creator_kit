# Analysis Report: ADR-016 TDD Implementation Plan

## 1. Intent Analysis (意図の深掘り)

ユーザーの真の意図は、「ADR/DesignDoc の管理コストを最小化し、実態 （タスク進捗）とドキュメント（ラベル）の乖離をゼロにすること」にあ る。特に、`integration` タスク의 완료という「設計・実装が完了し、監 査をパスした」タイミングを機械的に捉えることで、プロジェクトの全体 進捗をリアルタイムに可視化したいと考えている。

## 2. Gap Analysis (ギャップ分析)

- **機能ギャップ**: `L1AutomationUseCase` の正規表現不足、`RelayEngine` のフィードバック機構の欠如、`GitHubAdapter` のラベル属性定義の不足。
- **制約ギャップ**: `design-XXX` 形式が `DesignDoc` として `L1` 扱 いされるルールが、既存の `ADR` モデルのバリデーションを通過するように調整する必要がある。
- **非機能ギャップ**: 「状態の巻き戻り防止（冪等性）」を実現するた めの、フェーズ順序定義（`arch` < `spec` < `tdd`）のコード化が必要。

## 3. Formulated Hypotheses (解決策の仮説)

### Hypothesis A: Grounded (本命案)

- **Approach**:
  1. `L1AutomationUseCase.get_labels` の正規表現を拡張。
  2. `RelayEngine` にフェーズ順序を定義する `PHASE_ORDER = ["arch", "spec", "tdd"]` 定数を追加。
  3. `_handle_phase_transition` メソッドで、上位 Issue の現在のラベルを取得し、フェーズラベルを特定・比較して更新を行う。
- **Reasoning**: 最もシンプルかつ、ADR-016 の設計意図に忠実な実装。

### Hypothesis B: Leap (拡張案)

- **Approach**: フェーズ遷移と同時に、そのフェーズで作成されるべき 成果物のディレクトリ（`reqs/context/adr-XXX/{phase}/`）を自動スキャンし、不足があれば警告する。
- **Reasoning**: SSOT との実態乖離をより厳密に防止できる。

### Hypothesis C: Paradoxical (逆説案)

- **Approach**: ラベル管理を GitHub のネイティブ機能（GitHub Projects や Workflow）に任せる。
- **Reasoning**: アプリケーションコードを簡素化できるが、CLI が「リレー」の中心であるという本プロジェクトのアーキテクチャ方針に反する ため、採用は見送る。

## 4. Recommended Action (推奨アクション)

**Hypothesis A (Grounded)** を採用する。
TDD サイクルとして、まず `L1AutomationUseCase.get_labels` の単体テ ストを作成し、正規表現と初期ラベル付与の正しさを保証する。次に `RelayEngine` の単体テストで、異なる初期状態からのフェーズ遷移（および 巻き戻り防止）を検証する。

---

# Self-Review: Analysis Report

- **論理的飛躍はないか？**: 偵察レポートで得られた事実（正規表現の 不足など）から、具体的な解決策を導き出しており、飛躍はない。
- **リスクは特定されているか？**: 正規表現のミスによる `adr:design-016` のような不正ラベルの生成リスクを特定し、対策（条件分岐）を検討している。
- **ユーザー意図に即しているか？**: ADR-016 の「自動遷移」「DesignDoc対応」「冪等性」の 3 点をカバーしている。
