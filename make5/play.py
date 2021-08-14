from make5.utilities import read_frequencies, get_chance, get_subwords
from make5.compile_words import read_words
from make5.types import FrequencyDict, WordDict


MAX_LENGTH_BONUS = 5

class Score:
    def __init__(self, word: str, key: str, words: WordDict, frequency: FrequencyDict, max_length: int = 5) -> None:
        self.word = word
        self.key = key
        self.subwords = tuple(get_subwords(words, word))
        self.score = len(word) + MAX_LENGTH_BONUS if len(word) == max_length else 0
        self.chance = 1 - (1 - get_chance(key, word, frequency)) ** (max_length * max_length)  # Improve
        self.weighted_score = self.chance * self.score


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
        scores = [Score(word, key, words, frequency) for word in results]
        sorted_scores = sorted(scores, key=lambda s: s.weighted_score)
        for s in sorted_scores:
            print(f'{s.word:5} {s.weighted_score:5.1f} {s.score:4} {(s.chance * 100):6.2f}%: {s.subwords}')
        print(f'Total weighted score: {sum(s.weighted_score for s in scores):5.1f}')
        print()
