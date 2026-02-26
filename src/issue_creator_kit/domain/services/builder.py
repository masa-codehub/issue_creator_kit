import heapq

from issue_creator_kit.domain.exceptions import GraphError
from issue_creator_kit.domain.models.document import ADR, Task


class DocumentNode:
    """A node in the dependency graph representing a single document.

    Attributes:
        document: The Task or ADR document associated with this node.
        dependencies: Nodes that this node depends on (upstream).
        dependents: Nodes that depend on this node (downstream).
    """

    def __init__(self, document: Task | ADR):
        """Initializes a DocumentNode with a document."""
        self.document = document
        self.dependencies: list[DocumentNode] = []
        self.dependents: list[DocumentNode] = []

    @property
    def id(self) -> str:
        """Returns the ID of the document."""
        return self.document.id

    @property
    def title(self) -> str:
        """Returns the title of the document or its ID if title is missing."""
        return self.document.title or self.document.id


class TaskGraph:
    """Manages a collection of DocumentNodes and provides graph operations.

    Attributes:
        nodes: A dictionary mapping document IDs to their corresponding DocumentNode.
    """

    def __init__(self):
        """Initializes an empty TaskGraph."""
        self.nodes: dict[str, DocumentNode] = {}

    def add_document(self, doc: Task | ADR):
        """Adds a document to the graph as a node.

        Args:
            doc: The Task or ADR document to add.
        """
        if doc.id not in self.nodes:
            self.nodes[doc.id] = DocumentNode(doc)

    def add_edge(self, from_id: str, to_id: str):
        """Adds a dependency edge between two nodes.

        Args:
            from_id: The ID of the document that depends on another.
            to_id: The ID of the document that is being depended upon.
        """
        if from_id not in self.nodes or to_id not in self.nodes:
            return

        from_node = self.nodes[from_id]
        to_node = self.nodes[to_id]

        if to_node not in from_node.dependencies:
            from_node.dependencies.append(to_node)
        if from_node not in to_node.dependents:
            to_node.dependents.append(from_node)

    def validate(self, archived_ids: set[str] | dict[str, int]):
        """Validates the graph for self-references, orphan dependencies, and cycles.

        Args:
            archived_ids: A set of IDs for documents that are archived and thus valid dependencies.

        Raises:
            GraphError: If a self-reference, orphan dependency, or cycle is detected.
        """
        scanned_ids = set(self.nodes.keys())
        valid_ids = scanned_ids | set(archived_ids)

        for node_id, node in self.nodes.items():
            # Dependencies from depends_on
            deps = list(node.document.depends_on)
            # Add parent as implicit dependency for Tasks
            if isinstance(node.document, Task):
                deps.append(node.document.parent)

            for dep_id in deps:
                if dep_id == node_id:
                    raise GraphError(
                        f"SELF_REFERENCE '{node_id}' depends on itself",
                        code="SELF_REFERENCE",
                    )
                if dep_id not in valid_ids:
                    raise GraphError(
                        f"ORPHAN_DEPENDENCY '{dep_id}' referenced by '{node_id}' not found",
                        code="ORPHAN_DEPENDENCY",
                    )

        visited: set[str] = set()
        visiting: list[str] = []

        def detect_cycle(u_id: str):
            visited.add(u_id)
            visiting.append(u_id)

            node = self.nodes[u_id]
            for v_node in node.dependencies:
                v_id = v_node.id
                if v_id in visiting:
                    # Extract the cycle path from the visiting stack
                    cycle_start_index = visiting.index(v_id)
                    cycle_path = visiting[cycle_start_index:] + [v_id]
                    raise GraphError(
                        f"CYCLE_DETECTED circular dependency involves {cycle_path}",
                        code="CYCLE_DETECTED",
                    )
                if v_id not in visited:
                    detect_cycle(v_id)

            visiting.pop()

        for node_id in sorted(scanned_ids):
            if node_id not in visited:
                detect_cycle(node_id)

    def get_execution_order(self) -> list[str]:
        """Returns a list of document IDs in topological sorted order.

        Uses Kahn's algorithm with a min-heap to ensure lexicographical order
        for nodes with the same dependency level.

        Returns:
            A list of strings representing the execution order of document IDs.

        Raises:
            GraphError: If the graph contains a cycle.
        """
        in_degree = dict.fromkeys(self.nodes, 0)
        for node in self.nodes.values():
            for _ in node.dependencies:
                in_degree[node.id] += 1

        queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
        heapq.heapify(queue)

        result = []
        while queue:
            u_id = heapq.heappop(queue)
            result.append(u_id)

            for dependent in self.nodes[u_id].dependents:
                in_degree[dependent.id] -= 1
                if in_degree[dependent.id] == 0:
                    heapq.heappush(queue, dependent.id)

        if len(result) != len(self.nodes):
            raise GraphError(
                "CYCLE_DETECTED: Graph contains a circular dependency",
                code="CYCLE_DETECTED",
            )

        return result


class GraphBuilder:
    """Builder for constructing and validating a TaskGraph."""

    def build_graph(
        self, documents: list[Task | ADR], archived_ids: set[str] | dict[str, int]
    ) -> TaskGraph:
        """Builds a TaskGraph from a list of documents and archived IDs.

        Args:
            documents: A list of Task or ADR documents to include in the graph.
            archived_ids: A set of IDs for archived documents.

        Returns:
            A validated TaskGraph instance.
        """
        graph = TaskGraph()
        for doc in documents:
            graph.add_document(doc)

        for doc in documents:
            for dep_id in doc.depends_on:
                if dep_id not in archived_ids:
                    graph.add_edge(doc.id, dep_id)

            if isinstance(doc, Task) and doc.parent not in archived_ids:
                graph.add_edge(doc.id, doc.parent)

        graph.validate(archived_ids)
        return graph
