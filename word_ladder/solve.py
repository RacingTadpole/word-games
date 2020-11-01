from word_ladder.compile_words import read_words
from word_ladder.types import WordDict
from word_ladder.utilities import get_neighbors, build_rungs, get_ladders

from typing import Tuple


def input_start_and_target_words(words: WordDict) -> Tuple[str, str]:
    all_words = {w for word_list in words.values() for w in word_list}

    while True:
        start_word = input('Enter the starting word: ').lower()
        if not start_word:
            # If no start word, we'll exit gracefully.
            return '', ''
        neighbors = get_neighbors(start_word, words)
        if len(neighbors) > 1:
            break
        print(f'Sorry, there are no words next to "{start_word}". Choose another word.')
    if start_word not in all_words:
        print("(That word is not in the dictionary, but that's ok.)")

    while True:
        target_word = input('Enter the target word (if any): ').lower()
        if len(target_word) == 0:
            break
        if target_word in all_words:
            if len(target_word) == len(start_word):
                break
            else:
                print('Please choose a target word with the same length as the start word.')
        else:
            print('You need to choose a target word that is in the dictionary.')
    return (start_word, target_word)


if __name__ == '__main__':
    path = './data/words.txt'
    words = read_words(path)

    while True:
        start_word, target_word = input_start_and_target_words(words)
        if not start_word:
            print('Goodbye!')
            exit()

        final_rung = build_rungs(start_word, target_word, words)

        if len(final_rung.words) == 0:
            if (target_word):
                print('Could not do it!')
            final_rung = final_rung.previous
            if not final_rung:
                exit()
            print(f'Final words: {", ".join(sorted(final_rung.words))}')
            # Show the results for one of the words we could get to.
            target_word = list(final_rung.words)[0]

        print()
        ladders = get_ladders(final_rung, target_word)
        print(f'{len(ladders)} optimal solution(s) of length {len(ladders[0])} found:')
        for ladder in ladders:
            print(' → '.join(ladder))
        print()
