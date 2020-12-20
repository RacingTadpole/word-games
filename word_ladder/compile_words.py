"""
Run with:
    python -m word_ladder.solve
"""

from typing import Optional

from word_ladder.types import WordDict
from word_ladder.utilities import get_word_with_letter_missing


def add_to_words_dict(words: WordDict, word: str) -> WordDict:
    """
    >>> words = add_to_words_dict({}, 'dog')
    >>> words
    {'?og': ['dog'], 'd?g': ['dog'], 'do?': ['dog']}
    >>> words = add_to_words_dict(words, 'log')
    >>> words
    {'?og': ['dog', 'log'], 'd?g': ['dog'], 'do?': ['dog'], 'l?g': ['log'], 'lo?': ['log']}
    """
    for position in range(len(word)):
        key = get_word_with_letter_missing(word, position)
        if key in words:
            words[key] += [word]
        else:
            words[key] = [word]
    return words

def read_words(path: str, words: Optional[WordDict] = None) -> WordDict:
    updated_words = {} if words is None else words
    with open(path, 'r') as f:
        for word_with_return in f:
            word = word_with_return.strip()
            updated_words = add_to_words_dict(updated_words, word)
    return updated_words
