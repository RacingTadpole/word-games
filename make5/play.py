from collections import defaultdict
from typing import Iterator
from make5.utilities import read_frequencies, get_chance, get_subwords
from make5.compile_words import read_words
from make5.types import FrequencyDict, WordDict


MAX_LENGTH_BONUS = 5


def get_score(word: str, max_length: int = 5) -> int:
    return len(word) + (MAX_LENGTH_BONUS if len(word) == max_length else 0)

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
        self.start_index = start_index
        self.padded_word = pad_word(start_index, word, max_length)
        self.subwords = tuple(r[1] for r in get_subwords(words, word))
        self.score = get_score(word, max_length)
        self.chance = 1 - (1 - get_chance(key, word, frequency)) ** (max_length * max_length)  # Improve
        self.weighted_score = self.chance * self.score


def get_complete_choices(key: str, words: WordDict) -> Iterator[str]:
    """
    >>> from .utilities import _get_test_words
    >>> get_complete_choices('??og?', _get_test_words())
    ['blogs', 'clogs', 'slogs', 'adogs', 'blogo', 'clogo', 'slogo']
    """
    length = len(key)
    results = get_subwords(words, key)
    d = defaultdict(list)
    for start_index, word in results:
        d[(start_index, len(word))].append(word)
    # d[(0, length)] are the solutions so far.
    for min_length_so_far in range(2, length):
        for w in d.get((0, min_length_so_far), []):
            for start_index in range(1, length - 1):
                for comparison_length in range(min_length_so_far - start_index + 1, length):
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
    return d[(0, length)]


if __name__ == '__main__':
    words = read_words('./data/words.txt')
    frequency = read_frequencies('./make5/frequencies.txt')

    while True:
        key = input('Enter an expression, eg. ".rea.": ')
        key = key.replace('.', '?')
        if not key:
            print('Goodbye!')
            exit()
        
        results = get_subwords(words, key)
        choices = [Choice(word, key, start_index, words, frequency) for start_index, word in results]
        sorted_choices = sorted(choices, key=lambda s: s.weighted_score)
        for s in sorted_choices:
            print(f'{s.padded_word:5} {s.weighted_score:5.2f} {s.score:4} {(s.chance * 100):6.2f}%: {s.subwords}')
        print(f'Total weighted score: {sum(s.weighted_score for s in choices):5.1f}')
        print()
