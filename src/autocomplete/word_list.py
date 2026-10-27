from __future__ import annotations

import csv
from pathlib import Path

from .trie import Trie


def load_word_list(path: str | Path) -> tuple[Trie, int]:
    """Load a CSV file containing word[,score].

    Blank rows and rows with an empty first field are skipped.
    Invalid scores default to 0.0. Duplicate words update the existing score,
    and the returned count represents accepted rows (including duplicates).
    """
    trie = Trie()
    count = 0

    with open(path, "r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        for line_number, row in enumerate(reader, start=1):
            if not row or not row[0].strip():
                continue

            word = row[0].strip()
            score = 0.0

            if len(row) >= 2 and row[1].strip():
                try:
                    score = float(row[1])
                except ValueError:
                    # Keep the app usable with imperfect data.
                    score = 0.0

            trie.insert_word(word, score)
            count += 1

    return trie, count
