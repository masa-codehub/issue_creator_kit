package architecture.root

import future.keywords.if

# 許可される拡張子の定義
allowed_extensions := {".md", ".dsl", ".rego"}

# 1. design/ 配下全体のファイル拡張子制限
deny[msg] if {
	some i
	file := input.design_root_files[i]
	not file.is_dir
	name := file.name
	startswith(name, "design/")
	not is_allowed_extension(name)
	msg := sprintf("Forbidden file extension in design/: %v", [name])
}

is_allowed_extension(file) if {
	some ext
	allowed_extensions[ext]
	endswith(file, ext)
}

# ディレクトリ自体は許可
is_allowed_extension(file) if {
	endswith(file, "/")
}

# 2. design/ 直下には .md 以外のファイルを置かない (Only .md files or directories in root)
deny[msg] if {
	some i
	file := input.design_root_files[i]
	not file.is_dir
	name := file.name
	# design/ 直下のファイルのみを対象とする (Check only files directly under design/)
	startswith(name, "design/")
	subpath := substring(name, count("design/"), -1)
	not contains(subpath, "/")

	not endswith(name, ".md")
	msg := sprintf("Only .md files are allowed in design/ root, found file: %s", [name])
}

# 3. design/ から reqs/ への参照を禁止 (Forbid references to reqs/)
deny[msg] if {
	some i
	ref := input.design_references[i]
	contains(ref.path, "reqs/")
	msg := sprintf("Reference from design/ to reqs/ is forbidden: %s", [ref.path])
}
