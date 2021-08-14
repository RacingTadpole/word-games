import itertools
from typing import Iterator


def get_words_with_letters_missing(word: str, symbol: str = '?') -> Iterator[str]:
    """
    >>> list(get_words_with_letters_missing('dog'))
    ['?og', 'd?g', 'do?', '??g', '?o?', 'd??']
    """
    for r in range(1, len(word)): # ie. [1, 2, 3, ..., len(word) - 1]
        for replacement_indexes in itertools.combinations(range(len(word)), r):
            result = ''.join(symbol if i in replacement_indexes else word[i] for i in range(len(word)))
            yield result
