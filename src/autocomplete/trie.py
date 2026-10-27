from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TrieNode:
    children: dict[str, "TrieNode"] = field(default_factory=dict)
    is_end_of_word: bool = False
    score: float = float("inf")


class Trie:
    """Prefix tree whose suggestions are ranked by ascending score."""

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert_word(self, word: str, score: float = 0.0) -> None:
        if not word:
            raise ValueError("word must not be empty")

        node = self.root
        for char in word:
            node = node.children.setdefault(char, TrieNode())

        # Inserting an existing word updates its score.
        node.is_end_of_word = True
        node.score = score

    def autocomplete(self, prefix: str, top_n: int = 5) -> list[tuple[str, float]]:
        if top_n <= 0:
            return []

        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        results: list[tuple[str, float]] = []
        self._dfs(node, prefix, results)
        results.sort(key=lambda item: (item[1], item[0]))
        return results[:top_n]

    def _dfs(
        self,
        node: TrieNode,
        current_prefix: str,
        results: list[tuple[str, float]],
    ) -> None:
        if node.is_end_of_word:
            results.append((current_prefix, node.score))

        for char, child_node in node.children.items():
            self._dfs(child_node, current_prefix + char, results)
