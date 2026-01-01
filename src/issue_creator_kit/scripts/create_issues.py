# ruff: noqa: T201, ERA001
import os
import sys
from graphlib import TopologicalSorter
from pathlib import Path

import requests
import yaml

import issue_creator_kit.utils as utils

# Configuration
ISSUES_DIR = "reqs/tasks/_queue"
ARCHIVE_DIR = "reqs/tasks/archive"


def get_dependencies(files):
    """
    YAML メタデータから依存関係グラフを構築します。

    Returns:
        graph: {filename: {dependency_filename, ...}}
        file_map: {filename: full_path}
    """
    graph = {}
    file_map = {}

    for file_path_str in files:
        file_path = Path(file_path_str)
        filename = file_path.name
        file_map[filename] = str(file_path)

        try:
            metadata, _ = utils.load_document(file_path)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Warning: YAML parsing failed for {filename}: {e}", file=sys.stderr)
            continue
        except Exception as e:
            print(f"Warning: Failed to parse {filename}: {e}", file=sys.stderr)
            continue

        # depends_on キーの存在チェック (空リストの場合を考慮)
        depends_on = (
            metadata.get("depends_on")
            if "depends_on" in metadata
            else metadata.get("Depends-On")
        )

        deps = set()
        if depends_on:
            if isinstance(depends_on, list):
                # 新しい YAML リスト形式
                for dep in depends_on:
                    if isinstance(dep, str) and dep.endswith(".md"):
                        # 依存関係はファイル名のみで管理する（簡易化のため）
                        deps.add(Path(dep).name)
            elif isinstance(depends_on, str) and depends_on.lower() != "(none)":
                # 旧形式のカンマ区切り文字列
                cleaned = depends_on.replace("(", "").replace(")", "")
                for dep in cleaned.split(","):
                    dep = dep.strip()
                    if dep and dep.endswith(".md"):
                        deps.add(Path(dep).name)

        graph[filename] = deps

    return graph, file_map


def create_issue(filename, file_path_str, issue_map, repo, token):
    """
    Markdown ファイルから GitHub Issue を作成します。
    本文内の依存ファイル名を実際の Issue 番号に置換します。
    """
    api_url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    file_path = Path(file_path_str)
    try:
        metadata, content = utils.load_document(file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML in {filename}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error loading {filename}: {e}", file=sys.stderr)
        sys.exit(1)

    # タイトルの決定: メタデータ > 本文のH1 > ファイル名
    title = metadata.get("title")
    if not title:
        for line in content.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
    if not title:
        title = filename

    # 本文の準備: 依存ファイル名を Issue 番号に置換
    body = content
    for dep_filename, issue_number in issue_map.items():
        body = body.replace(dep_filename, f"#{issue_number}")

    data = {
        "title": title,
        "body": body,
    }

    # ラベルの設定
    if "labels" in metadata:
        labels = metadata["labels"]
        if isinstance(labels, list):
            data["labels"] = [
                lbl for lbl in labels if isinstance(lbl, str) and lbl.strip()
            ]
        elif isinstance(labels, str):
            data["labels"] = [lbl.strip() for lbl in labels.split(",") if lbl.strip()]

    print(f"Creating issue for {filename}...")
    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 201:
        issue = response.json()
        issue_number = issue["number"]
        print(f"Success! Created issue #{issue_number} for {filename}")
        return issue_number

    print(
        f"Failed to create issue for {filename}. Status: {response.status_code}",
        file=sys.stderr,
    )
    print(response.text, file=sys.stderr)
    sys.exit(1)


def main():
    repo = os.environ.get("GITHUB_REPOSITORY")
    token = os.environ.get("GH_TOKEN")

    if not repo or not token:
        print(
            "Error: GITHUB_REPOSITORY or GH_TOKEN environment variable is missing.",
            file=sys.stderr,
        )
        sys.exit(1)

    # 1. 対象ファイルの特定 (再帰的に走査)
    files = [
        str(f)
        for f in Path(ISSUES_DIR).rglob("*.md")
        if f.is_file() and "_queue" in str(f)
    ]

    if not files:
        print("No issue files found in queue.")
        return

    print(f"Found {len(files)} files to process.")

    # 2. 依存関係グラフの構築
    graph, file_map = get_dependencies(files)

    # 3. トポロジカルソート
    ts = TopologicalSorter(graph)
    try:
        create_order = list(ts.static_order())
    except Exception as e:
        print(f"Error resolving dependencies (Cycle detected?): {e}", file=sys.stderr)
        sys.exit(1)

    # 4. 順序に従って Issue を作成
    issue_map = {}  # {filename: issue_number}

    for filename in create_order:
        if filename not in file_map:
            # 既にアーカイブされている可能性があるため、アーカイブ内を検索して Issue 番号を取得することを検討すべきだが、
            # 現状はスキップする（後続の置換には使えない）
            continue

        file_path_str = file_map[filename]
        file_path = Path(file_path_str)

        # Issue の作成
        issue_number = create_issue(filename, file_path_str, issue_map, repo, token)

        # 5. アーカイブへの移動 (ディレクトリ構造を維持)
        try:
            # ISSUES_DIR からの相対パスを取得
            rel_path = file_path.relative_to(ISSUES_DIR)
            target_dir = Path(ARCHIVE_DIR) / rel_path.parent

            utils.safe_move_file(file_path, target_dir, overwrite=True)
            print(f"Moved {filename} to {target_dir}")

            # 作成した Issue 番号をドキュメントに追記
            archived_path = target_dir / filename
            utils.update_metadata(archived_path, {"issue": f"#{issue_number}"})

            issue_map[filename] = issue_number
        except Exception as e:
            print(f"Error archiving {filename}: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
