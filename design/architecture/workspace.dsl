workspace "Issue Creator Kit" {
    model {
        # Actors
        architect = person "Architect" "The person who defines design and tasks."
        developer = person "Developer" "The person who implements issues and performs PR reviews."
        agent = person "AI Agent" "The agent that decomposes tasks, creates PRs, and implements issues."

        # Systems
        ick = softwareSystem "Issue Creator Kit" "A toolkit to automate document movement and issue creation." {
            tags "Layer:System"

            cli = container "CLI Entrypoint" "Handles user input and starts UseCases." "Python/Click" {
                tags "Layer:Interface"
                
                main = component "CLI/Runner" "Entry point and command definitions." "cli.py, __main__.py" {
                    tags "Layer:Interface" "Type:Component"
                }
            }
            usecase = container "UseCase Layer" "Application-specific business rules." "Python" {
                tags "Layer:UseCase"
                
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
            domain = container "Domain Layer" "Domain models, entities, and services." "Python/Pydantic" {
                tags "Layer:Domain"
                
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
            infra = container "Infrastructure Layer" "External communications (GitHub, Git, FS)." "Python" {
                tags "Layer:Infrastructure"
                
                gh_adapter = component "GitHubAdapter" "Wrapper for GitHub REST API." "github_adapter.py" {
                    tags "Layer:Infrastructure" "Type:Component"
                }
                fs_adapter = component "FileSystemAdapter" "Wrapper for physical file operations." "filesystem.py" {
                    tags "Layer:Infrastructure" "Type:Component"
                }
            }

            # Relationships between components
            main -> l1_auto "Requests issue creation"
            main -> task_act "Requests activation"
            main -> scanner_uc "Requests scan"
            
            l1_auto -> scanner_svc "Scans files"
            l1_auto -> interfaces "Creates/Searches issues"
            
            task_act -> builder "Builds dependency graph"
            task_act -> renderer "Generates issue body"
            task_act -> interfaces "Creates issues"
            task_act -> interfaces "Moves files to archive"
            task_act -> l1_sync "Syncs L1 checklist"
            
            l1_sync -> interfaces "Updates issue body"
            
            scanner_uc -> scanner_svc "Scans files"
            
            builder -> doc_model "Uses model"
            renderer -> doc_model "Uses model"
            scanner_svc -> doc_model "Generates model"
            
            gh_adapter -> interfaces "Implements"
            fs_adapter -> interfaces "Implements"

            # Container relationships (for summary)
            cli -> usecase "Starts UseCase"
            cli -> infra "Initializes for DI"
            usecase -> domain "Uses domain models"
            domain -> domain "Executes logic between entities"
            infra -> domain "Converts to domain model"
        }
        github = softwareSystem "GitHub" "External platform for repo management, CI/CD, and Issues/PRs." {
            tags "External"
        }
        fs = softwareSystem "File System" "Where documents (ADR/Task) are physically stored." {
            tags "External"
        }

        # Relationships (Actors to Systems)
        architect -> github "Pushes designs and issues" "Git/HTTPS"
        developer -> github "Pushes implementations and reviews PRs" "Git/HTTPS"
        agent -> github "Decomposes tasks and implements issues" "Git/HTTPS"

        # Relationships (Systems to Systems)
        github -> ick "Triggers workflows" "GitHub Actions"
        ick -> github "Creates issues, operates on PRs" "REST API"
        ick -> fs "Searches, reads, and moves files" "File I/O"

        # Relationships (Containers to Systems)
        infra -> github "Calls REST API" "HTTPS"
        infra -> fs "Operates physical files" "File I/O"
    }

    views {
        systemContext ick "SystemContext" {
            include *
            autoLayout lr
        }

        container ick "ContainerView" {
            include *
            autoLayout lr
        }

        component cli "CLI_ComponentView" {
            include *
            autoLayout lr
        }

        component usecase "UseCase_ComponentView" {
            include *
            autoLayout lr
        }

        component domain "Domain_ComponentView" {
            include *
            autoLayout lr
        }

        component infra "Infrastructure_ComponentView" {
            include *
            autoLayout lr
        }

        styles {
            element "External" {
                background #999999
                color #ffffff
            }
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "Person" {
                shape Person
                background #08427b
                color #ffffff
            }
        }
    }

    !docs docs/
}
