package architecture.container

import future.keywords.if

# 1. Domain 層は他のどの層にも依存してはならない (Pure Domain)
deny[msg] if {
	rel := input.relationships[_]
	rel.source.tags[_] == "Layer:Domain"
	not is_domain_internal(rel.destination)
	msg := sprintf("Domain layer must not depend on other layers: %s -> %s", [rel.source.name, rel.destination.name])
}

is_domain_internal(dest) if {
	dest.tags[_] == "Layer:Domain"
}

# 2. UseCase 層は Interface 層に依存してはならない
deny[msg] if {
	rel := input.relationships[_]
	rel.source.tags[_] == "Layer:UseCase"
	rel.destination.tags[_] == "Layer:Interface"
	msg := sprintf("UseCase layer must not depend on Interface layer: %s -> %s", [rel.source.name, rel.destination.name])
}

# 3. Infrastructure 層は Interface 層に依存してはならない
deny[msg] if {
	rel := input.relationships[_]
	rel.source.tags[_] == "Layer:Infrastructure"
	rel.destination.tags[_] == "Layer:Interface"
	msg := sprintf("Infrastructure layer must not depend on Interface layer: %s -> %s", [rel.source.name, rel.destination.name])
}

# 4. システム全体として外部への直接依存は Infrastructure 経由のみとする
deny[msg] if {
	rel := input.relationships[_]
	is_runtime_element(rel.source)
	not is_infrastructure(rel.source)
	rel.destination.tags[_] == "External"
	msg := sprintf("Direct communication to External systems must be via Infrastructure: %s -> %s", [rel.source.name, rel.destination.name])
}

is_runtime_element(el) if {
	el.tags[_] == "Container"
}

is_runtime_element(el) if {
	el.tags[_] == "Component"
}

is_infrastructure(source) if {
	source.tags[_] == "Layer:Infrastructure"
}
