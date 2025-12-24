# 開発環境のセットアップガイド

このドキュメントでは、このプロジェクトの**ローカル開発環境**をセットアップする手順について説明します。

> このプロジェクトは Docker を利用した開発もサポートしています。詳細は `docker-compose.yml` を参照してください。

## 1. 前提条件

開発を始める前に、以下のツールがインストールされていることを確認してください。

- [Git](https://git-scm.com/)
- [GitHub CLI](https://cli.github.com/)
- [Python](https://www.python.org/) (バージョン 3.12 以上)
- [Node.js](https://nodejs.org/) (npm を含む)

## 2. セットアップ手順

### ステップ1: リポジトリの準備

> **コントリビューター向けの注意**
> プロジェクトに貢献する場合は、まずリポジトリをご自身のアカウントにフォークし、そのフォークをクローンしてください。GitHub CLI を使うと、`gh repo fork masa-codehub/gemini_agent --clone` コマンドでフォークとクローンを一度に行えます。

まだクローンしていない場合は、以下のコマンドでリポジトリをローカルマシンにクローンします。

```bash
git clone https://github.com/masa-codehub/gemini_agent.git
cd gemini_agent
```

### ステップ2: 認証設定

開発には GitHub および Google Cloud への認証が必要です。

1.  **GitHub CLI 認証:**
    以下のコマンドを実行し、ブラウザの指示に従って GitHub にログインします。これにより、Git 操作がスムーズになります。

    ```bash
    gh auth login
    gh auth setup-git
    ```

2.  **Google Cloud 認証:**
    プロジェクトで Google Cloud のサービスを利用するため、認証スクリプトを実行します。

    ```bash
    bash ./.build/setup_gemini_auth.sh
    ```

### ステップ3: 依存関係のインストール

プロジェクトで必要なツールとライブラリをインストールします。

1.  **Gemini CLI のインストール:**
    Node.js のパッケージマネージャーである npm を使って、Google Gemini CLI をグローバルにインストールします。ビルドの再現性を高めるため、バージョンを固定します。

    ```bash
    npm install -g @google/gemini-cli@latest
    ```

2.  **Python 依存関係のインストール:**
    Python のパッケージマネージャーである pip を使って、必要なライブラリをインストールします。

    ```bash
    # 外部リポジトリの依存関係をインストール
    pip install -r .build/repositories.txt

    # プロジェクトの依存関係をインストール (開発用ツールも含む)
    pip install -e .[dev]
    ```

### ステップ4: Git フックの設定

コミット前にコードの品質を自動的にチェックするため、pre-commit フックを設定します。

```bash
pre-commit install
```

### ステップ5: 環境変数の設定

アプリケーションは環境変数から設定を読み込みます。サンプルファイルをコピーして、独自の設定ファイルを作成してください。

1.  `.env.sample` を `.env` にコピーします。
    ```bash
    cp .build/context/.env.sample .build/context/.env
    ```

2.  `.build/context/.env` ファイルを開き、ご自身の環境に合わせて各変数の値を編集します。

## 3. 実行方法

すべてのセットアップが完了したら、以下のコマンドでエージェントを起動できます。

```bash
python main.py
```

これにより、`main.py` が実行され、サーバーに接続してタスクの処理を開始します。