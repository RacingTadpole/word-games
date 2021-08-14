import itertools
from make5.types import FrequencyDict
from typing import Iterator


def get_words_with_letters_missing(word: str, symbol: str = '?') -> Iterator[str]:
    """
    >>> list(get_words_with_letters_missing('dog'))
    ['dog', '?og', 'd?g', 'do?', '??g', '?o?', 'd??']
    """
    for r in range(0, len(word)): # ie. [0, 1, 2, 3, ..., len(word) - 1]
        for replacement_indexes in itertools.combinations(range(len(word)), r):
            result = ''.join(symbol if i in replacement_indexes else word[i] for i in range(len(word)))
            yield result


def read_frequencies(path: str) -> FrequencyDict:
    """
    >>> import os
    >>> dir_path = os.path.dirname(os.path.realpath(__file__))
    >>> freq = read_frequencies(os.path.join(dir_path, 'frequencies.txt'))
    >>> freq['a'], freq['z']
    (0.1, 0.02)
    """
    d = {}
    with open(path, 'r') as f:
        for line in f:
            components = line.strip().split(',')
            d[components[0]] = int(components[1])
    total = sum(v for v in d.values())
    return {k: v / total for k, v in d.items()}
