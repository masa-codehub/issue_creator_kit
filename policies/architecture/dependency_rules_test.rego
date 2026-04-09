package architecture.dependency_test

import data.architecture.dependency as policy
import future.keywords.if

# Test: Allow Domain component to depend on another Domain component
test_domain_to_domain_allowed if {
	test_input := {
		"relationships": [
			{
				"source": {"name": "DocumentModel", "tags": ["Layer:Domain", "Type:Component"]},
				"destination": {"name": "ScannerService", "tags": ["Layer:Domain", "Type:Component"]}
			}
		]
	}
	count(policy.deny) == 0 with input as test_input
}

# Test: Deny Domain component to depend on UseCase component
test_domain_to_usecase_denied if {
	test_input := {
		"relationships": [
			{
				"source": {"name": "DocumentModel", "tags": ["Layer:Domain", "Type:Component"]},
				"destination": {"name": "L1AutomationUseCase", "tags": ["Layer:UseCase", "Type:Component"]}
			}
		]
	}
	policy.deny["Domain component must not depend on other layers: DocumentModel -> L1AutomationUseCase"] with input as test_input
}

# Test: Deny UseCase component to depend on Infra component
# In this policy, UseCase components must not depend on any Infrastructure components.
test_usecase_to_infra_denied if {
	test_input := {
		"relationships": [
			{
				"source": {"name": "L1AutomationUseCase", "tags": ["Layer:UseCase", "Type:Component"]},
				"destination": {"name": "GitHubAdapter", "tags": ["Layer:Infrastructure", "Type:Component"]}
			}
		]
	}
	policy.deny["UseCase component must not depend on Infrastructure component: L1AutomationUseCase -> GitHubAdapter"] with input as test_input
}
