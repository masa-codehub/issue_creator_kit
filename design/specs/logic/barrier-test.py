import json
import logging
import sys
from pathlib import Path

# Configure logging to output to stdout
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def get_allowed_destinations(arch, component_id):
    model = arch.get("model", {})
    systems = model.get("softwareSystems", [])
    for system in systems:
        containers = system.get("containers", [])
        for container in containers:
            components = container.get("components", [])
            for component in components:
                if component.get("id") == component_id:
                    rels = component.get("relationships", [])
                    return {rel.get("destinationId") for rel in rels}
    return set()


def get_all_components(arch):
    components_map = {}
    model = arch.get("model", {})
    systems = model.get("softwareSystems", [])
    for system in systems:
        containers = system.get("containers", [])
        for container in containers:
            components = container.get("components", [])
            for component in components:
                components_map[component.get("name")] = component.get("id")
                # Also index by identifier if available
                if (
                    "properties" in component
                    and "structurizr.dsl.identifier" in component["properties"]
                ):
                    components_map[
                        component["properties"]["structurizr.dsl.identifier"]
                    ] = component.get("id")
    return components_map


def test_barrier():
    structurizr_path = Path("design/architecture/structurizr.json")
    spec_path = Path("design/specs/logic/state-machine.json")

    if not spec_path.exists():
        logger.error(f"RED: Specification file {spec_path} does not exist yet.")
        return False

    with open(structurizr_path) as f:
        arch = json.load(f)

    with open(spec_path) as f:
        sm = json.load(f)

    components_map = get_all_components(arch)

    # Target component: TaskActivationUseCase (structurizr.dsl.identifier: task_act, ID: 9)
    orchestrator_id = components_map.get("task_act")
    if not orchestrator_id:
        logger.error("ERROR: task_act component not found in structurizr.json")
        return False

    allowed_ids = get_allowed_destinations(arch, orchestrator_id)
    logger.info(f"Allowed destination IDs for task_act: {allowed_ids}")

    # Extract invokes from XState JSON
    invokes = []

    def find_invokes(obj):
        if isinstance(obj, dict):
            if "invoke" in obj:
                inv = obj["invoke"]
                if isinstance(inv, list):
                    invokes.extend(inv)
                else:
                    invokes.append(inv)
            for v in obj.values():
                find_invokes(v)
        elif isinstance(obj, list):
            for item in obj:
                find_invokes(item)

    find_invokes(sm)

    violations = []
    for inv in invokes:
        src = inv.get("src")
        if src:
            # Assume src matches component name or identifier in structurizr
            dest_id = components_map.get(src)
            if not dest_id:
                violations.append(f"Invoiced target '{src}' not found in model.")
            elif dest_id not in allowed_ids:
                violations.append(
                    f"Invoiced target '{src}' (ID: {dest_id}) is not a permitted dependency in structurizr.json."
                )

    if violations:
        logger.error("RED: Barrier violations found:")
        for v in violations:
            logger.error(f"  - {v}")
        return False

    logger.info("GREEN: All invokes are within the allowed architecture boundaries.")
    return True


if __name__ == "__main__":
    if not test_barrier():
        sys.exit(1)
    sys.exit(0)
