from make5.utilities import read_frequencies
from typing import Iterable, Iterator, Sequence
from make5.compile_words import read_words
from make5.types import FrequencyDict, WordDict


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


if __name__ == '__main__':
    words = read_words('./data/words.txt')
    frequency = read_frequencies('./make5/frequencies.txt')

    while True:
        key = input('Enter an expression, eg. "?rea?": ')
        if not key:
            print('Goodbye!')
            exit()
        
        results = words[key]
        # TODO: allow non-5-letter words too
        scores = [{
            'subwords': tuple(get_subwords(words, result)),
            'chance': get_chance(key, result, frequency),
            'word': result,
        } for result in results]
        sorted_scores = sorted(scores, key=lambda x: get_score(x['subwords']))
        for s in sorted_scores:
            print(f'{s["word"]:5} {get_score(s["subwords"]):4} {(s["chance"] * 100):.4f}%: {s["subwords"]}')
        print()
