package architecture.container_test

import data.architecture.container as policy
import future.keywords.if

# Test: Allow valid Domain internal dependency
test_domain_internal_allowed if {
	test_input := {
		"relationships": [
			{
				"source": {"name": "Parser", "tags": ["Layer:Domain"]},
				"destination": {"name": "Document", "tags": ["Layer:Domain"]}
			}
		]
	}
	count(policy.deny) == 0 with input as test_input
}

# Test: Deny Domain to UseCase dependency
test_domain_to_usecase_denied if {
	test_input := {
		"relationships": [
			{
				"source": {"name": "DomainModel", "tags": ["Layer:Domain"]},
				"destination": {"name": "UseCase", "tags": ["Layer:UseCase"]}
			}
		]
	}
	policy.deny["Domain layer must not depend on other layers: DomainModel -> UseCase"] with input as test_input
}

# Test: Deny UseCase to Interface dependency
test_usecase_to_interface_denied if {
	test_input := {
		"relationships": [
			{
				"source": {"name": "UseCase", "tags": ["Layer:UseCase"]},
				"destination": {"name": "CLI", "tags": ["Layer:Interface"]}
			}
		]
	}
	policy.deny["UseCase layer must not depend on Interface layer: UseCase -> CLI"] with input as test_input
}

# Test: Allow Infra to External dependency
test_infra_to_external_allowed if {
	test_input := {
		"relationships": [
			{
				"source": {"name": "GitHubAdapter", "tags": ["Layer:Infrastructure", "Container"]},
				"destination": {"name": "GitHub API", "tags": ["External"]}
			}
		]
	}
	count(policy.deny) == 0 with input as test_input
}

# Test: Deny UseCase to External direct dependency
test_usecase_to_external_denied if {
	test_input := {
		"relationships": [
			{
				"source": {"name": "UseCase", "tags": ["Layer:UseCase", "Container"]},
				"destination": {"name": "GitHub API", "tags": ["External"]}
			}
		]
	}
	policy.deny["Direct communication to External systems must be via Infrastructure: UseCase -> GitHub API"] with input as test_input
}

# Test: Deny Infra to Interface dependency (Rule 3)
test_infra_to_interface_denied if {
	test_input := {
		"relationships": [
			{
				"source": {"name": "GitHubAdapter", "tags": ["Layer:Infrastructure"]},
				"destination": {"name": "CLI", "tags": ["Layer:Interface"]}
			}
		]
	}
	policy.deny["Infrastructure layer must not depend on Interface layer: GitHubAdapter -> CLI"] with input as test_input
}

# Test: Deny Interface to External direct dependency (Rule 4)
test_interface_to_external_denied if {
	test_input := {
		"relationships": [
			{
				"source": {"name": "CLI", "tags": ["Layer:Interface", "Container"]},
				"destination": {"name": "GitHub API", "tags": ["External"]}
			}
		]
	}
	policy.deny["Direct communication to External systems must be via Infrastructure: CLI -> GitHub API"] with input as test_input
}
