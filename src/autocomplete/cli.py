from __future__ import annotations

import curses
import csv
import os
from pathlib import Path
import unicodedata

from .trie import Trie
from .word_list import load_word_list

DEFAULT_WORD_LIST = "icf.txt"


def is_word_separator(char: str) -> bool:
    return char.isspace() or unicodedata.category(char).startswith("P")


def current_word_prefix(text: str) -> str:
    prefix: list[str] = []
    for char in reversed(text):
        if is_word_separator(char):
            break
        prefix.append(char)
    return "".join(reversed(prefix))


def safe_addnstr(
    stdscr: curses.window,
    y: int,
    x: int,
    text: str,
    width: int,
    attr: int = 0,
) -> None:
    height, screen_width = stdscr.getmaxyx()
    if y < 0 or y >= height or width <= 0 or x < 0 or x >= screen_width:
        return
    try:
        stdscr.addnstr(y, x, text, min(width, screen_width - x - 1), attr)
    except curses.error:
        # Terminal may resize between getmaxyx() and addnstr().
        pass


def run_autocomplete_ui(stdscr: curses.window, trie: Trie) -> None:
    try:
        curses.curs_set(1)
    except curses.error:
        pass

    stdscr.keypad(True)
    stdscr.timeout(-1)
    query = ""

    while True:
        height, width = stdscr.getmaxyx()
        stdscr.erase()

        safe_addnstr(
            stdscr, 0, 0,
            "Autocomplete | ESC: menu | Ctrl+U: limpar",
            width - 1, curses.A_BOLD,
        )
        safe_addnstr(stdscr, 2, 0, f"> {query}", width - 1)

        prefix = current_word_prefix(query)
        if prefix:
            suggestions = trie.autocomplete(prefix, top_n=5)
            safe_addnstr(
                stdscr, 4, 0,
                f'Sugestões para "{prefix}" (top 5):',
                width - 1,
            )
            if suggestions:
                for index, (word, score) in enumerate(suggestions):
                    if 5 + index >= height:
                        break
                    safe_addnstr(
                        stdscr, 5 + index, 0,
                        f"  {index + 1}. {word} (score: {score:g})",
                        width - 1,
                    )
            else:
                safe_addnstr(
                    stdscr, 5, 0,
                    "  (nenhuma palavra encontrada)", width - 1,
                )
        else:
            safe_addnstr(
                stdscr, 4, 0,
                "Digite uma palavra. Espaços e pontuação reiniciam as sugestões.",
                width - 1,
            )

        cursor_x = min(2 + len(query), max(width - 1, 0))
        if height > 2 and width > 0:
            try:
                stdscr.move(2, cursor_x)
            except curses.error:
                pass
        stdscr.refresh()

        try:
            key = stdscr.get_wch()
        except curses.error:
            continue

        if key == "\x1b":
            break
        if key == "\x03":
            raise KeyboardInterrupt
        if key == "\x15":
            query = ""
        elif key in (curses.KEY_BACKSPACE, "\x7f", "\b"):
            query = query[:-1]
        elif isinstance(key, str) and key.isprintable():
            query += key


def show_menu(loaded_path: str | None, word_count: int) -> None:
    print("\n=== Autocomplete com Trie ===")
    print(f"Lista: {loaded_path or '(nenhuma carregada)'} | palavras: {word_count}")
    print("1. Carregar lista de palavras")
    print("2. Iniciar programa")
    print("0. Sair")


def clear_terminal() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def main() -> None:
    trie: Trie | None = None
    loaded_path: str | None = None
    word_count = 0

    while True:
        clear_terminal()
        show_menu(loaded_path, word_count)
        choice = input("Opção: ").strip()

        if choice == "1":
            path = input(f"Caminho do arquivo [{DEFAULT_WORD_LIST}]: ").strip()
            path = path or DEFAULT_WORD_LIST

            if not Path(path).is_file():
                print(f"Arquivo não encontrado: {path}")
                input("Pressione Enter para continuar...")
                continue

            try:
                trie, word_count = load_word_list(path)
            except (OSError, UnicodeError, csv.Error) as error:
                print(f"Não foi possível ler o arquivo: {error}")
                input("Pressione Enter para continuar...")
                continue

            loaded_path = path
            print(f"Lista carregada: {word_count} linhas válidas.")
            input("Pressione Enter para continuar...")

        elif choice == "2":
            if trie is None:
                print("Carregue uma lista de palavras primeiro (opção 1).")
                input("Pressione Enter para continuar...")
                continue
            try:
                curses.wrapper(run_autocomplete_ui, trie)
            except KeyboardInterrupt:
                print("\nPrograma interrompido.")
                input("Pressione Enter para continuar...")

        elif choice == "0":
            break
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")
