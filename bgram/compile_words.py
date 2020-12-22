# This is the same method of compiling words as boggle.
from typing import Iterable, Optional, Dict

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

# Some sample words to make it easy to write succinct tests.
sample_words = ['egg', 'tree', 'feet', 'flee', 'fleet', 'flag', 'flea', 'flog', 'ogre', 'on']

def compile_words(word_list: Optional[Iterable[str]] = None) -> Dict:
    """
    Useful for testing. Lets you create a words dict from a list of words.
    """
    words = {}
    for word in word_list or sample_words:
        words = add_to_words_subtree(words, word)
    return words

def read_words(path: str, words: Optional[Dict] = None) -> Dict:
    """
    Read words from a text file and compile them into the format we need.
    Ignore words without any vowels (eg. dr and mrs).
    """
    vowels = 'aeiouy'
    updated_words = {} if words is None else words
    with open(path, 'r') as f:
        for word_with_return in f:
            word = word_with_return.strip().lower()
            if any(vowel in word for vowel in vowels):
                updated_words = add_to_words_subtree(updated_words, word)
    return updated_words

