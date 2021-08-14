from make5.utilities import read_frequencies, get_score, get_chance, get_subwords
from make5.compile_words import read_words
from make5.types import FrequencyDict, WordDict


class Score:
    def __init__(self, word: str, key: str, words: WordDict, frequency: FrequencyDict) -> None:
        self.word = word
        self.key = key
        self.subwords = tuple(get_subwords(words, word))
        self.score = get_score(self.subwords)
        self.chance = get_chance(key, word, frequency) * 28  # Improve
        self.weighted_score = self.chance * self.score


if __name__ == '__main__':
    words = read_words('./data/words.txt')
    frequency = read_frequencies('./make5/frequencies.txt')

    while True:
        key = input('Enter an expression, eg. "?rea?": ')
        if not key:
            print('Goodbye!')
            exit()
        
        results = words.get(key, [])
        # TODO: allow non-5-letter words too
        scores = [Score(word, key, words, frequency) for word in results]
        sorted_scores = sorted(scores, key=lambda s: s.score)
        for s in sorted_scores:
            print(f'{s.word:5} {get_score(s.subwords):4} {(s.chance * 100):5.1f}%: {s.subwords}')
        print(f'Total weighted score: {sum(s.weighted_score for s in scores):5.1f}')
        print()
