# External Systems
github = softwareSystem "GitHub" "External platform for repo management, CI/CD, and Issues/PRs." {
    tags "External"
}
fs = softwareSystem "File System" "Where documents (ADR/Task) are physically stored." {
    tags "External"
}

# Issue Creator Kit System (Boundary)
ick = softwareSystem "Issue Creator Kit" "A toolkit to automate document movement and issue creation." {
    tags "Layer:System"
    
    # Placeholder for containers - will be filled by !include in workspace.dsl
}

# Global Relationships (Actors to Systems)
architect -> github "Pushes designs and issues" "Git/HTTPS"
developer -> github "Pushes implementations and reviews PRs" "Git/HTTPS"
agent -> github "Decomposes tasks and implements issues" "Git/HTTPS"

# Global Relationships (Systems to Systems)
github -> ick "Triggers workflows" "GitHub Actions"
ick -> github "Creates issues, operates on PRs" "REST API"
ick -> fs "Searches, reads, and moves files" "File I/O"
