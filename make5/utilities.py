import itertools
from make5.types import FrequencyDict, WordDict
from typing import Iterable, Iterator


def get_words_with_letters_missing(word: str, symbol: str = '?') -> Iterator[str]:
    """
    >>> list(get_words_with_letters_missing('dog'))
    ['dog', '?og', 'd?g', 'do?', '??g', '?o?', 'd??']
    """
    for r in range(0, len(word)): # ie. [0, 1, 2, 3, ..., len(word) - 1]
        for replacement_indexes in itertools.combinations(range(len(word)), r):
            result = ''.join(symbol if i in replacement_indexes else word[i] for i in range(len(word)))
            yield result


def get_subwords(words: WordDict, word: str, min_length: int = 3) -> Iterator[str]:
    """
    >>> import os
    >>> dir_path = os.path.dirname(os.path.realpath(__file__))
    >>> words = read_words(os.path.join(dir_path, 'test_data.txt'))
    >>> list(get_subwords(words, 'skits'))
    ['ski', 'kit', 'its', 'skit', 'kits', 'skits']
    >>> list(get_subwords(words, 'alogs'))
    ['log', 'logs']
    """
    for length in range(min_length, len(word) + 2):
        for start_index in range(0, len(word) - length + 1):
            candidate = word[start_index:start_index + length]
            if candidate in words:
                yield candidate


def get_score(words: Iterable[str]) -> int:
    """
    >>> get_score(['log', 'logs'])
    7
    """
    return sum(len(word) for word in words)


def get_chance(key: str, word: str, frequency: FrequencyDict, symbol: str = '?') -> float:
    """
    >>> import os
    >>> dir_path = os.path.dirname(os.path.realpath(__file__))
    >>> frequency = read_frequencies(os.path.join(dir_path, 'frequencies.txt'))
    >>> get_chance('???f?', 'loafs', frequency)
    9.6e-06
    """
    x = 1
    for i in range(len(word)):
        if key[i] == symbol:
            x = x * frequency[word[i]]
    return x


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
