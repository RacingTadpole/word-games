from boggle.replacements import replace_special
from typing import Optional, Dict

def add_to_words_subtree(words_subtree: Dict, rest_of_word: str) -> Dict:
    """
    >>> add_to_words_subtree({}, 'b')
    {'b': {'.': None}}
    >>> add_to_words_subtree({}, 'bar')
    {'b': {'a': {'r': {'.': None}}}}
    >>> add_to_words_subtree({'r': {'.': None}}, 'n')
    {'r': {'.': None}, 'n': {'.': None}}
    >>> add_to_words_subtree({'r': {'.': None}}, 'ns')
    {'r': {'.': None}, 'n': {'s': {'.': None}}}
    >>> add_to_words_subtree({'b': {'a': {'r': {'.': None}}}}, 'be')
    {'b': {'a': {'r': {'.': None}}, 'e': {'.': None}}}
    >>> add_to_words_subtree({'b': {'a': {'r': {'.': None}}}}, 'am')
    {'b': {'a': {'r': {'.': None}}}, 'a': {'m': {'.': None}}}
    """
    if len(rest_of_word) == 0:
        return {'.': None}
    letter = rest_of_word[0]
    next_subtree = words_subtree.get(letter, {})
    words_subtree[letter] = add_to_words_subtree(next_subtree, rest_of_word[1:])
    return words_subtree

def read_words(path: str, words: Optional[Dict] = None) -> Dict:
    updated_words = {} if words is None else words
    with open(path, 'r') as f:
        for word_with_return in f:
            word = replace_special(word_with_return.strip().lower())
            updated_words = add_to_words_subtree(updated_words, word)
    return updated_words
