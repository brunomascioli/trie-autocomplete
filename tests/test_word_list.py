from autocomplete.word_list import load_word_list


def test_load_word_list(tmp_path):
    word_file = tmp_path / "words.csv"
    word_file.write_text(
        'café,1.5\n'
        'casa,2\n'
        ',9\n'
        'carro,invalid\n'
        '\n',
        encoding="utf-8",
    )

    trie, count = load_word_list(word_file)

    assert count == 3
    assert trie.autocomplete("ca") == [
        ("carro", 0.0),
        ("café", 1.5),
        ("casa", 2.0),
    ]
