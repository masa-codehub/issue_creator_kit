# Containers
cli = container "CLI Entrypoint" "Handles user input and starts UseCases." "Python/Click" {
    tags "Layer:Interface"
}
usecase = container "UseCase Layer" "Application-specific business rules." "Python" {
    tags "Layer:UseCase"
}
domain = container "Domain Layer" "Domain models, entities, and services." "Python/Pydantic" {
    tags "Layer:Domain"
}
infra = container "Infrastructure Layer" "External communications (GitHub, Git, FS)." "Python" {
    tags "Layer:Infrastructure"
}
database = container "Metadata Database" "Stores ADR and Task metadata for traceability." "SQLite" {
    tags "Layer:Infrastructure" "Type:Database"
}

# Container Relationships (Global)
cli -> usecase "Starts UseCase"
cli -> infra "Initializes for DI"
usecase -> domain "Uses domain models"
domain -> domain "Executes logic between entities"
infra -> domain "Converts to domain model"
infra -> database "Persists metadata" "SQL/SQLite"

# External System Connections
infra -> github "Calls REST API" "HTTPS"
infra -> fs "Operates physical files" "File I/O"
