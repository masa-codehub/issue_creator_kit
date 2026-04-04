package spec.behavior

import future.keywords.if
import future.keywords.in

# Tracetest YAML (input) の service.name が structurizr.json (data.model.softwareSystems) に存在することを検証する

# 1. Tracetest YAML の spec.specs 配下の各 selector から service.name を抽出し検証
deny[msg] if {
	some spec in input.spec.specs
	service_name := get_service_name(spec.selector)
	not is_valid_service(service_name)
	msg := sprintf("Service '%s' defined in Tracetest selector is not found in structurizr.json", [service_name])
}

# selector から service.name="xyz" または service.name = 'xyz' を抽出する正規表現
get_service_name(selector) = name if {
	# span[service.name="backend-api" name="process-checkout"] 形式などを想定
	# スペースの有無やシングル/ダブルクォートを許容
	matches := regex.find_all_string_submatch_n(`service\.name\s*=\s*["']([^"']+)["']`, selector, 1)
	count(matches) > 0
	name := matches[0][1]
}

# structurizr.json 内の有効な要素名・IDの集合
is_valid_service(name) if {
	some system in data.model.softwareSystems
	some container in system.containers
	container.name == name
}

is_valid_service(name) if {
	some system in data.model.softwareSystems
	some container in system.containers
	container.properties["structurizr.dsl.identifier"] == name
}

is_valid_service(name) if {
	some system in data.model.softwareSystems
	some container in system.containers
	some component in container.components
	component.name == name
}

is_valid_service(name) if {
	some system in data.model.softwareSystems
	some container in system.containers
	some component in container.components
	component.properties["structurizr.dsl.identifier"] == name
}
