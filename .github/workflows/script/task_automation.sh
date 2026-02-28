#!/bin/bash
set -euo pipefail

# ==============================================================================
# Task Automation Script
# ==============================================================================
# ADR-014準拠: YAMLからのインラインスクリプト排除と、パラメータ経由の制御
#
# このスクリプトは issue-kit の process または relay コマンドを実行します。
# 呼び出し元 (GitHub Actions) から引数として必要なコンテキストを受け取ります。
#
# 引数 (Arguments):
#   $1 - COMMAND      : 実行するモード ("process" または "relay")
#   $2 - FLAG         : 実行フラグ ("--execute" または "--dry-run")
#   $3 - ROOT_DIR     : スキャン対象のルートディレクトリ (例: "reqs")
#   $4 - CONFIG_PATH  : 設定ファイルのパス
#   $5 - ISSUE_NO     : リレー実行時の対象 Issue 番号 (オプション)
# ==============================================================================

COMMAND="${1:-process}"
FLAG="${2:---dry-run}"
ROOT_DIR="${3:-reqs}"
CONFIG_PATH="${4:-.github/issue-kit-config.json}"
ISSUE_NO="${5:-}"

echo "=== Issue Creator Kit Automation ==="
echo "Mode        : $COMMAND"
echo "Flag        : $FLAG"
echo "Root Dir    : $ROOT_DIR"
echo "Config Path : $CONFIG_PATH"
echo "Issue No    : ${ISSUE_NO:-(none)}"
echo "===================================="

if [ "$COMMAND" = "relay" ]; then
    # リレーモード: クローズされた Issue に依存する後続タスクを起動する
    if [ -z "$ISSUE_NO" ]; then
        echo "Error: Issue number is required for relay command."
        exit 1
    fi
    echo "Running Relay Engine for Issue #$ISSUE_NO..."
    uv run issue-kit relay --issue-no "$ISSUE_NO" "$FLAG"

elif [ "$COMMAND" = "process" ]; then
    # プロセスモード: ディレクトリをスキャンし、新規 Issue の作成とタスクの更新を行う
    echo "Running Process Engine for directory: $ROOT_DIR..."
    uv run issue-kit process "$FLAG" --root "$ROOT_DIR" --config-path "$CONFIG_PATH"

else
    echo "Error: Unknown command '$COMMAND'. Expected 'process' or 'relay'."
    exit 1
fi
