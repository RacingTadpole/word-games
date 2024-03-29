from typing import Sequence, Union
from make5.utilities import SYMBOL, get_chance, get_subwords, get_full_length_combos
from make5.types import FrequencyDict, WordDict
from make5.score import get_score


def pad_word(start_index: int, word: str, max_length: int, pad_symbol = '.'):
    """
    >>> pad_word(1, 'foo', 5)
    '.foo.'
    >>> pad_word(2, 'foo', 5)
    '..foo'
    """
    return pad_symbol * start_index + word + pad_symbol * (max_length - start_index - len(word))


class Choice:
    def __init__(self, word: str, key: str, start_index: int, words: WordDict, frequency: FrequencyDict, max_length: int = 5) -> None:
        self.word = word
        self.key = key
        self.max_length = max_length
        self.start_index = start_index
        self.subwords = tuple(r[1] for r in get_subwords(words, word))
        self.score = sum(get_score(w, max_length) for w in self.subwords)
        self.chance = 1 - (1 - get_chance(key, word, frequency)) ** (max_length * max_length)  # Improve
        self.adjusted_score = self.chance * self.score


def get_sorted_choices(key: str, required_index: Union[int, None], words: WordDict, frequency: FrequencyDict) -> Sequence[Choice]:
    length = len(key)
    subwords = tuple(get_subwords(words, key))
    full_length_results = list(get_full_length_combos(subwords, length))
    partial_results = [pad_word(start_index, word, length)
        for start_index, word in subwords 
        if len(word) != length]
    if required_index is not None:
        partial_results = [word for word in partial_results if word[required_index] != SYMBOL]
    results = partial_results + full_length_results
    choices = [Choice(word, key, 0, words, frequency) for word in results]
    sorted_choices = sorted(choices, key=lambda s: s.adjusted_score)
    return sorted_choices


def print_choices(sorted_choices: Sequence[Choice]) -> None:
    for s in sorted_choices:
        print(f'{pad_word(s.start_index, s.word, s.max_length):5} {s.adjusted_score:5.2f} {s.score:4} {(s.chance * 100):6.2f}%: {s.subwords}')
    print(f'Total adjusted score: {sum(s.adjusted_score for s in sorted_choices):5.1f}')
