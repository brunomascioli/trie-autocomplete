# Trie Autocomplete

A terminal-based autocomplete application implemented in Python using a Trie (prefix tree).

## Features

- Prefix-based search using a Trie.
- Suggestions ranked by ascending score.
- Alphabetical ordering for equal scores.
- Interactive terminal interface built with `curses`.
- Word list loading from a CSV file.

## Requirements

- Python 3.10 or newer.
- A terminal with `curses` support.

On some Windows installations, `curses` is not available by default. Linux and macOS are the simplest environments to run this project.

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project and development dependency:

```bash
python -m pip install -e ".[dev]"
```

## Run

```bash
python main.py
```

The default word list is `icf.txt`. Choose option 1 to load a word list, then option 2 to start autocomplete.

## Word-list format

Each CSV row contains a word and an optional numeric score:

```csv
apple,1.5
application,2.0
apply,1.0
```

Lower scores appear first. Equal scores are ordered alphabetically. A missing or invalid score defaults to `0.0`. Inserting a duplicate word updates its score.

## Controls

- `ESC`: return to the menu.
- `Ctrl+U`: clear the current query.
- `Backspace`: delete the last character.

## Tests

```bash
pytest
```

## Design

- `trie.py`: data structure and autocomplete ranking.
- `word_list.py`: CSV loading.
- `cli.py`: menu and `curses` interface.
- `tests/`: automated tests.

## License

See `LICENSE`.
