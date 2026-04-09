# UseCase Container Components
extend usecase {
    l1_auto = component "L1AutomationUseCase" "Automatically creates L1 issues from ADRs." "l1_automation_usecase.py" {
        tags "Layer:UseCase" "Type:Component"
    }
    task_act = component "TaskActivationUseCase" "Creates L2/L3 issues from task drafts." "task_activation_usecase.py" {
        tags "Layer:UseCase" "Type:Component"
    }
    scanner_uc = component "ScannerUseCase" "Scans physical files and summarizes the current state." "scanner_usecase.py" {
        tags "Layer:UseCase" "Type:Component"
    }
    validator = component "Validator" "Validates document consistency and dependencies." "validator.py" {
        tags "Layer:UseCase" "Type:Component"
    }
}

# Inbound Relationships
main -> l1_auto "Requests issue creation"
main -> task_act "Requests activation"
main -> scanner_uc "Requests scan"
