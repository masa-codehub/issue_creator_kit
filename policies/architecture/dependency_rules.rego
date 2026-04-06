package architecture.dependency

import future.keywords.if

# 1. Domain 層は他のどの層にも依存してはならない (Pure Domain at Component level)
deny[msg] if {
	rel := input.relationships[_]
	rel.source.tags[_] == "Layer:Domain"
	rel.source.tags[_] == "Type:Component"
	not is_domain_internal(rel.destination)
	msg := sprintf("Domain component must not depend on other layers: %s -> %s", [rel.source.name, rel.destination.name])
}

is_domain_internal(dest) if {
	dest.tags[_] == "Layer:Domain"
}

# 2. UseCase 層は Infrastructure 具象に依存してはならない (Must use interfaces)
deny[msg] if {
	rel := input.relationships[_]
	rel.source.tags[_] == "Layer:UseCase"
	rel.source.tags[_] == "Type:Component"
	rel.destination.tags[_] == "Layer:Infrastructure"
	rel.destination.tags[_] == "Type:Component"
	msg := sprintf("UseCase component must not depend on Infrastructure component: %s -> %s", [rel.source.name, rel.destination.name])
}
