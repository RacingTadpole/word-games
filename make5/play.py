from make5.utilities import read_frequencies, get_chance, get_subwords, get_full_length_combos
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
        self.score = sum(get_score(w, max_length) for w in self.subwords)
        self.chance = 1 - (1 - get_chance(key, word, frequency)) ** (max_length * max_length)  # Improve
        self.weighted_score = self.chance * self.score


def print_combos(key: str, words: WordDict, frequency: FrequencyDict):
    length = len(key)
    subwords = list(get_subwords(words, key))
    full_length_results = list(get_full_length_combos(subwords, length))
    partial_results = [pad_word(start_index, word, length)
        for start_index, word in subwords 
        if len(word) != length]
    results = partial_results + full_length_results
    choices = [Choice(word, key, 0, words, frequency) for word in results]
    sorted_choices = sorted(choices, key=lambda s: s.weighted_score)
    for s in sorted_choices:
        print(f'{s.padded_word:5} {s.weighted_score:5.2f} {s.score:4} {(s.chance * 100):6.2f}%: {s.subwords}')
    print(f'Total weighted score: {sum(s.weighted_score for s in choices):5.1f}')


if __name__ == '__main__':
    words = read_words('./data/words.txt')
    frequency = read_frequencies('./make5/frequencies.txt')

    while True:
        print()
        key = input('Enter an expression, eg. ".re..": ')
        key = key.replace('.', '?')
        if not key:
            print('Goodbye!')
            exit()
        letter = input('Enter the new letter (if any): ')
        print()

        if letter:
            for position in range(len(key)):
                if key[position] == '?':
                    this_key = ''.join(letter if i == position else key[i] for i in range(len(key)))
                    print(this_key)
                    print_combos(this_key, words, frequency)
        else:
            print_combos(key, words, frequency)
