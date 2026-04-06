package db.schema_test

import data.db.schema
import future.keywords.if
import future.keywords.in

# 正常系: すべての要件を満たす場合
test_valid_schema if {
    count(schema.deny) == 0 with input as valid_input
                            with data.model as mock_model
}

# 異常系: 監査カラム不足
test_missing_audit_columns if {
    some msg in schema.deny with input as invalid_audit_input
                            with data.model as mock_model
    contains(msg, "missing audit columns")
}

# 異常系: TableGroup がアーキテクチャに存在しない
test_invalid_table_group if {
    some msg in schema.deny with input as invalid_group_input
                            with data.model as mock_model
    contains(msg, "not found in architecture containers")
}

# 異常系: 命名規則違反 (camelCase)
test_naming_convention_violation if {
    some msg in schema.deny with input as invalid_naming_input
                            with data.model as mock_model
    contains(msg, "must be in snake_case")
}

# Mock Data (matches structurizr.json model structure)
mock_model := {
    "softwareSystems": [
        {
            "containers": [
                {
                    "name": "Metadata Database",
                    "tags": "Type:Database"
                }
            ]
        }
    ]
}

valid_input := {
    "table_groups": {"Metadata Database": {}},
    "tables": {
        "l1_documents": {
            "columns": [
                {"name": "id"},
                {"name": "created_at"},
                {"name": "updated_at"}
            ]
        }
    }
}

invalid_audit_input := {
    "table_groups": {"Metadata Database": {}},
    "tables": {
        "l1_documents": {
            "columns": [
                {"name": "id"}
            ]
        }
    }
}

invalid_group_input := {
    "table_groups": {"Unknown Database": {}},
    "tables": {
        "l1_documents": {
            "columns": [
                {"name": "id"},
                {"name": "created_at"},
                {"name": "updated_at"}
            ]
        }
    }
}

invalid_naming_input := {
    "table_groups": {"Metadata Database": {}},
    "tables": {
        "l1Document": {
            "columns": [
                {"name": "id"},
                {"name": "created_at"},
                {"name": "updatedAt"}
            ]
        }
    }
}
