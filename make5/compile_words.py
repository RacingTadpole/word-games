import itertools
from make5.utilities import SYMBOL
from typing import Optional, Iterator
from make5.types import WordDict


def get_words_with_letters_missing(word: str) -> Iterator[str]:
    """
    >>> list(get_words_with_letters_missing('dog'))
    ['dog', '?og', 'd?g', 'do?', '??g', '?o?', 'd??', '???']
    """
    for r in range(0, len(word) + 1): # ie. [0, 1, 2, 3, ..., len(word)]
        for replacement_indexes in itertools.combinations(range(len(word)), r):
            result = ''.join(SYMBOL if i in replacement_indexes else word[i] for i in range(len(word)))
            yield result


def add_to_words_dict(words: WordDict, word: str) -> WordDict:
    """
    >>> words = add_to_words_dict({}, 'dog')
    >>> words
    {'dog': ['dog'], '?og': ['dog'], 'd?g': ['dog'], 'do?': ['dog'], '??g': ['dog'], '?o?': ['dog'], 'd??': ['dog'], '???': ['dog']}
    >>> words = add_to_words_dict(words, 'log')
    >>> words
    {'dog': ['dog'], '?og': ['dog', 'log'], 'd?g': ['dog'], 'do?': ['dog'], '??g': ['dog', 'log'], '?o?': ['dog', 'log'], 'd??': ['dog'], '???': ['dog', 'log'], 'log': ['log'], 'l?g': ['log'], 'lo?': ['log'], 'l??': ['log']}
    """
    for key in get_words_with_letters_missing(word):
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
            if len(word) <= 5:
                updated_words = add_to_words_dict(updated_words, word)
    return updated_words
