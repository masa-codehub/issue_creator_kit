# Domain Container Components
extend domain {
    doc_model = component "DocumentModel" "Domain model representing ADRs and tasks." "models/document.py" {
        tags "Layer:Domain" "Type:Component"
    }
    interfaces = component "Interfaces" "Abstraction for external adapters (GitHub, FileSystem)." "interfaces.py" {
        tags "Layer:Domain" "Type:Component" "Type:Interface"
    }
    builder = component "GraphBuilder" "Builds dependency graphs between documents." "services/builder.py" {
        tags "Layer:Domain" "Type:Component"
    }
    renderer = component "IssueRenderer" "Renders issue body with metadata." "services/renderer.py" {
        tags "Layer:Domain" "Type:Component"
    }
    scanner_svc = component "ScannerService" "Extracts metadata from physical files." "services/scanner.py" {
        tags "Layer:Domain" "Type:Component"
    }
    l1_sync = component "L1SyncService" "Updates the parent issue (L1) checklist." "services/l1_sync.py" {
        tags "Layer:Domain" "Type:Component"
    }
}

# Inbound Relationships (from UseCase)
l1_auto -> scanner_svc "Scans files"
l1_auto -> interfaces "Creates/Searches issues"

task_act -> builder "Builds dependency graph"
task_act -> renderer "Generates issue body"
task_act -> interfaces "Creates issues"
task_act -> interfaces "Moves files to archive"
task_act -> l1_sync "Syncs L1 checklist"

l1_sync -> interfaces "Updates issue body"
scanner_uc -> scanner_svc "Scans files"

# Internal Domain Relationships
builder -> doc_model "Uses model"
renderer -> doc_model "Uses model"
scanner_svc -> doc_model "Generates model"
