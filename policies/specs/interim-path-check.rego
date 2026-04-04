package spec.interim_path

import future.keywords.if

# 移行期間中のドキュメント配置・リンクパスの正当性をチェックする暫定ポリシー
# 入力(input)は、検証対象のファイルパス(path)と内容(content)を持つオブジェクトを想定

# 1. 廃止予定のパス docs/specs/ または docs/architecture/ への Markdown リンク参照がある場合に警告
deny[msg] if {
	some path in ["docs/specs/", "docs/architecture/"]
	# Markdown リンク等の“参照”だけを対象にし、コードブロック等での言及は許容する
	regex.match(sprintf("\\[[^\\]]*\\]\\([^)]*%s[^)]*\\)", [path]), input.content)
	msg := sprintf("Obsolete path detected in %s: '%s'. Use 'design/specs/' or 'design/architecture/' instead.", [input.path, path])
}

# 2. adr-017 関連の成果物が適切なディレクトリ配下に配置されていない場合に警告
# (このルールはファイルパス自体をチェックする)
deny[msg] if {
	contains(input.path, "adr-017")
	not startswith(input.path, "design/")
	not startswith(input.path, "policies/")
	not startswith(input.path, "reqs/")
	msg := sprintf("ADR-017 artifact %s must be placed under design/, policies/, or reqs/.", [input.path])
}
