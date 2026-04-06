package db.schema

import future.keywords.if
import future.keywords.contains
import future.keywords.in

# 負の制約: 監査カラムの必須化
deny contains msg if {
    some name, table in input.tables
    audit_columns := {"created_at", "updated_at"}
    existing_columns := {col.name | some col in table.columns}
    missing := audit_columns - existing_columns
    count(missing) > 0
    msg := sprintf("Table '%v' is missing audit columns: %v", [name, missing])
}

# 防波堤遵守: TableGroup 名が structurizr.json のデータベースコンテナ名と一致すること
deny contains msg if {
    some group_name, _ in input.table_groups
    not container_exists(group_name)
    msg := sprintf("TableGroup '%v' not found in architecture containers (structurizr.json)", [group_name])
}

# structurizr.json から Database タグを持つコンテナ名の集合を取得
container_exists(name) if {
    some system in data.model.softwareSystems
    some container in system.containers
    container.name == name
    tags := container.tags
    tags != null
    regex.match("(^|,\\s*)Type:Database(,|$)", tags)
}

# 命名規則: テーブル名とカラム名は snake_case
deny contains msg if {
    some name, _ in input.tables
    not is_snake_case(name)
    msg := sprintf("Table name '%v' must be in snake_case", [name])
}

deny contains msg if {
    some table_name, table in input.tables
    some column in table.columns
    column_name := column.name
    not is_snake_case(column_name)
    msg := sprintf("Column name '%v' in table '%v' must be in snake_case", [column_name, table_name])
}

is_snake_case(str) if {
    regex.match("^[a-z0-9_]+$", str)
}
