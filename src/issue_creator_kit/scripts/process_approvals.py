import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from github import Github, GithubException

import issue_creator_kit.utils as utils


def process_single_file(
    file_path: Path, approved_dir: Path, repo_name: str, token: str
) -> None:
    """
    承認されたドキュメントを処理します。

    1. ドキュメントの読み込み
    2. ステータスを「承認済み」、日付を当日に更新
    3. 承認済みディレクトリへ移動
    4. GitHub Issue の作成
    5. ドキュメントに Issue 番号を追記

    失敗した場合は、ファイルの移動をロールバックします。
    """

    # 1. ドキュメントの読み込み
    metadata, content = utils.load_document(file_path)
    title = metadata.get("title") or metadata.get("タイトル") or file_path.stem

    # 2. ステータスと日付の更新
    today = datetime.now().strftime("%Y-%m-%d")
    updates = {"Status": "承認済み", "Date": today}

    # 既存のキー名に合わせる（互換性維持）
    if "status" in metadata:
        updates["status"] = "承認済み"
    if "date" in metadata:
        updates["date"] = today
    if "Last Updated" in metadata:
        updates["Last Updated"] = today
    if "last_updated" in metadata:
        updates["last_updated"] = today

    utils.update_metadata(file_path, updates)

    # 3. ファイルの移動
    moved_path = utils.safe_move_file(file_path, approved_dir)
    print(f"Moved file to: {moved_path}")

    # 4. GitHub Issue の作成
    try:
        g = Github(token)
        repo = g.get_repo(repo_name)

        relative_path = str(moved_path)

        # content が 200 文字を超える場合のみ ... を付与
        summary = content[:200]
        if len(content) > 200:
            summary += "..."

        issue_body = (
            f"Tracking issue for approved document: {relative_path}\n\n"
            f"Original Content Summary:\n{summary}"
        )

        issue = repo.create_issue(
            title=title, body=issue_body, labels=["documentation", "approved"]
        )
        print(f"Created Issue #{issue.number}")

        # 5. Issue 番号の追記
        utils.update_metadata(moved_path, {"Issue": f"#{issue.number}"})
        if "issue" in metadata:
            utils.update_metadata(moved_path, {"issue": f"#{issue.number}"})
        print(f"Updated document with Issue #{issue.number}")

    except Exception as e:
        # ロールバック処理
        print(f"Error during Issue creation: {e}", file=sys.stderr)
        try:
            # 元の場所に戻す
            utils.safe_move_file(moved_path, file_path.parent, overwrite=True)
            print(f"Rolled back file move to: {file_path}", file=sys.stderr)
        except Exception as rollback_error:
            print(f"Failed to rollback file move: {rollback_error}", file=sys.stderr)
        raise e


def main():
    parser = argparse.ArgumentParser(description="承認済みドキュメントを処理します。")
    parser.add_argument("file_path", type=Path, help="承認するドキュメントへのパス")
    parser.add_argument(
        "--approved-dir",
        type=Path,
        default=Path("reqs/design/_approved"),
        help="承認済みファイルを移動するディレクトリ",
    )
    parser.add_argument("--repo", required=True, help="GitHub リポジトリ (owner/repo)")
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_TOKEN"),
        help="GitHub トークン。セキュリティのため、GITHUB_TOKEN 環境変数の使用を推奨します。",
    )

    args = parser.parse_args()

    if not args.token:
        print(
            "Error: GitHub Token is required (via --token or GITHUB_TOKEN env var)",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        process_single_file(args.file_path, args.approved_dir, args.repo, args.token)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except GithubException as e:
        # トークン情報が漏洩しないように、例外メッセージの扱いに注意
        print(f"GitHub API Error: {e.status} {e.data}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
