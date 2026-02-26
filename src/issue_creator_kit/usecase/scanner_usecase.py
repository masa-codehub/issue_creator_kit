from pathlib import Path
from typing import NamedTuple

from issue_creator_kit.domain.models.document import ADR, Task
from issue_creator_kit.domain.services.builder import GraphBuilder, TaskGraph
from issue_creator_kit.domain.services.scanner import FileSystemScanner
from issue_creator_kit.domain.services.visualizer import Visualizer


class ScanResult(NamedTuple):
    execution_order: list[str]
    documents: list[Task | ADR]


class ScannerUseCase:
    """UseCase for scanning documents and handling graph operations."""

    def __init__(
        self,
        scanner: FileSystemScanner,
        builder: GraphBuilder,
        visualizer: Visualizer,
    ):
        self.scanner = scanner
        self.builder = builder
        self.visualizer = visualizer

    def _scan_and_build_graph(
        self, root_path: Path | str
    ) -> tuple[TaskGraph, list[Task | ADR]]:
        """
        Helper to scan files and build the dependency graph.
        """
        documents, archived_ids = self.scanner.scan(root_path)
        graph = self.builder.build_graph(documents, archived_ids)
        return graph, documents

    def get_process_list(self, root_path: Path | str) -> ScanResult:
        """
        Scan and build execution order.

        Returns:
            ScanResult containing execution order (IDs) and the list of documents.
        """
        graph, documents = self._scan_and_build_graph(root_path)
        order = graph.get_execution_order()

        # We want to return documents in the execution order
        doc_map = {doc.id: doc for doc in documents}
        ordered_docs = [doc_map[doc_id] for doc_id in order]

        return ScanResult(execution_order=order, documents=ordered_docs)

    def visualize_graph(self, root_path: Path | str) -> str:
        """
        Scan, build graph and return Mermaid visualization.
        """
        graph, _ = self._scan_and_build_graph(root_path)
        return self.visualizer.to_mermaid(graph)
