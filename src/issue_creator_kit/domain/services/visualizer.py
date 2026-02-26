from issue_creator_kit.domain.services.builder import TaskGraph


class Visualizer:
    """Generates Mermaid diagrams from a TaskGraph."""

    def to_mermaid(self, graph: TaskGraph) -> str:
        """Converts a TaskGraph into a Mermaid graph TD string.

        Args:
            graph: The TaskGraph instance to visualize.

        Returns:
            A string containing the Mermaid diagram definition.
        """
        lines = ["graph TD"]

        # 1. Node definitions (sorted by ID for determinism)
        for node_id in sorted(graph.nodes.keys()):
            node = graph.nodes[node_id]
            title = self._escape_title(node.title)
            lines.append(f'    {node_id}["{title}"]')

        # 2. Edge definitions (sorted by FromID then ToID for determinism)
        edges = []
        for node_id, node in graph.nodes.items():
            for dep in node.dependencies:
                edges.append((node_id, dep.id))

        for from_id, to_id in sorted(edges):
            lines.append(f"    {from_id} --> {to_id}")

        return "\n".join(lines)

    def _escape_title(self, title: str) -> str:
        """Escapes special characters in a title for Mermaid compatibility.

        Args:
            title: The title string to escape.

        Returns:
            The escaped title string.
        """
        if not title:
            return ""

        # Replacements based on Mermaid requirements
        return (
            title.replace('"', '\\"')
            .replace("[", "(")
            .replace("]", ")")
            .replace("\n", "<br/>")
        )
