from collections import defaultdict
from functools import lru_cache
from typing import Iterator, Tuple
from make5.types import FrequencyDict, WordDict

SYMBOL = '?'

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
    ['ado', 'too', 'dog', 'log', 'blog', 'clog', 'slog', 'dogs', 'logs', 'blogs', 'clogs', 'slogs']
    """
    yield from (
        (start, w) for start, subkey in get_subsets(key, min_length)
            for w in words.get(subkey, []))


def get_chance(key: str, word: str, frequency: FrequencyDict) -> float:
    """
    >>> import os
    >>> dir_path = os.path.dirname(os.path.realpath(__file__))
    >>> frequency = read_frequencies(os.path.join(dir_path, 'tiles.txt'))
    >>> get_chance('???f?', 'loafs', frequency)
    9.6e-06
    >>> get_chance('???f?', '?oafs', frequency)
    0.00024
    """
    x = 1
    for i in range(len(word)):
        if key[i] == SYMBOL:
            x = x * frequency.get(word[i], 1)
    return x


@lru_cache(maxsize=5000)
def get_full_length_combos(subwords: Tuple[Tuple[int, str]], full_length: int) -> Iterator[str]:
    """
    This returns key-length combinations that make more than one word.
    Ie. it is missing the single words which do not fit with any others.
    >>> from .utilities import _get_test_words
    >>> subwords = get_subwords(_get_test_words(), '??og?')
    >>> get_full_length_combos(subwords, 5)
    ['blogs', 'clogs', 'slogs', 'adogs', 'blogo', 'clogo', 'slogo']
    >>> subwords = get_subwords(_get_test_words(), '?????')
    >>> get_full_length_combos(subwords, 5)
    ['blogs', 'clogs', 'doggy', 'logos', 'skits', 'slogs', 'adogs', 'blogo', 'clogo', 'slogo']
    """
    d = defaultdict(list)
    for start_index, word in subwords:
        d[(start_index, len(word))].append(word)
    # d[(0, length)] are the solutions so far.
    for min_length_so_far in range(2, full_length):
        for w in d.get((0, min_length_so_far), []):
            for start_index in range(1, full_length - 1):
                for comparison_length in range(min_length_so_far - start_index + 1, full_length):
                    for w2 in d.get((start_index, comparison_length), []):
                        # print((0, min_length_so_far, w), (start_index, comparison_length, w2), list(range(start_index, min_length_so_far)))
                        if all(w[i] == w2[i - start_index] for i in range(start_index, min_length_so_far)):
                            # These two words match at all common positions.
                            # If it's a new combination, add it to the dictionary d.
                            new_combo = w + w2[min_length_so_far - 1:]
                            new_key = (0, len(new_combo))
                            if new_combo not in d[new_key]:
                                # print(new_key, new_combo)
                                d[new_key].append(new_combo)
    return d[(0, full_length)]


def read_frequencies(path: str) -> FrequencyDict:
    """
    >>> import os
    >>> dir_path = os.path.dirname(os.path.realpath(__file__))
    >>> freq = read_frequencies(os.path.join(dir_path, 'tiles.txt'))
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
