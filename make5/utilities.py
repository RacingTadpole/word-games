from make5.types import FrequencyDict, WordDict
from typing import Iterator, Tuple

def _get_test_words() -> WordDict:
    """
    >>> _get_test_words()['?og']
    ['dog', 'log']
    """
    import os
    from .compile_words import read_words
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return read_words(os.path.join(dir_path, 'test_data.txt'))


def get_subsets(key: str, min_length: int = 3) -> Iterator[Tuple[int, str]]:
    """
    >>> list(get_subsets('?kits'))
    [(0, '?ki'), (1, 'kit'), (2, 'its'), (0, '?kit'), (1, 'kits'), (0, '?kits')]
    """
    for length in range(min_length, len(key) + 2):
        for start_index in range(0, len(key) - length + 1):
            yield start_index, key[start_index:start_index + length]


def get_subwords(words: WordDict, key: str, min_length: int = 3) -> Iterator[Tuple[int, str]]:
    """
    >>> words = _get_test_words()
    >>> list(get_subwords(words, 'skits'))
    [(0, 'ski'), (1, 'kit'), (2, 'its'), (0, 'skit'), (1, 'kits'), (0, 'skits')]
    >>> [z[1] for z in get_subwords(words, '??ogs')]
    ['ado', 'dog', 'log', 'blog', 'clog', 'slog', 'dogs', 'logs', 'blogs', 'clogs', 'slogs']
    """
    yield from (
        (start, w) for start, subkey in get_subsets(key, min_length)
            for w in words.get(subkey, []))


def get_chance(key: str, word: str, frequency: FrequencyDict, symbol: str = '?') -> float:
    """
    >>> import os
    >>> dir_path = os.path.dirname(os.path.realpath(__file__))
    >>> frequency = read_frequencies(os.path.join(dir_path, 'frequencies.txt'))
    >>> get_chance('???f?', 'loafs', frequency)
    9.6e-06
    >>> get_chance('???f?', '?oafs', frequency)
    0.00024
    """
    x = 1
    for i in range(len(word)):
        if key[i] == symbol:
            x = x * frequency.get(word[i], 1)
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
