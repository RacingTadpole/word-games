from dataclasses import dataclass
from make5.types import FrequencyDict, WordDict
from typing import Any, Dict, Optional, Sequence, Tuple
from make5.choice import get_sorted_choices
from make5.utilities import SYMBOL, read_frequencies
from make5.compile_words import read_words

ALL_LETTERS = 'abcdefghijklmnopqrstuvwxyz'


def replace(key: str, position: int, letter: str) -> str:
    """
    >>> replace('floop', 0, 'p')
    'ploop'
    >>> replace('floop', 3, 'r')
    'florp'
    >>> replace('floop', 4, 'r')
    'floor'
    """
    return key[:position] + letter + key[position + 1:]


@dataclass(frozen=True)
class Crosshair:
    score: float
    row: Sequence[str]
    col: Sequence[str]


def get_crosshairs(
    row_key: str,
    col_key: str,
    row_index: int,
    col_index: int,
    allowed_letters: Optional[Sequence[str]],
    words: WordDict,
    frequency: FrequencyDict
) -> Dict[str, Crosshair]:
    """
    >>> from .utilities import _get_test_words
    >>> import os
    >>> dir_path = os.path.dirname(os.path.realpath(__file__))
    >>> frequency = read_frequencies(os.path.join(dir_path, 'test_tiles.txt'))
    >>> result = get_crosshairs('??og?', '?oo??', 0, 1, None, _get_test_words(), frequency)
    >>> items = result.items()
    >>> c = sorted(items, key=lambda x: x[1].score, reverse=True)
    >>> [(cc[0], f'{cc[1].score:3.1f}', cc[1].row[:3], cc[1].col[:3]) for cc in c if cc[1].score > 0]
    [('l', '31.7', ['.logo', '.logs', 'slog.'], ['loo..', 'look.']), ('d', '11.2', ['.dogs', '.dog.', 'ado..'], []), ('t', '6.7', ['.toga'], ['too..']), ('o', '4.3', ['too..', 'loo..'], [])]
    """
    if allowed_letters is None:
        allowed_letters = ALL_LETTERS
    result_dict: dict[str, float] = {}
    for letter in allowed_letters:
        this_row_key = replace(row_key, col_index, letter)
        row_choices = get_sorted_choices(this_row_key, col_index, words, frequency)
        row_score = sum(s.adjusted_score for s in row_choices)

        this_col_key = replace(col_key, row_index, letter)
        col_choices = get_sorted_choices(this_col_key, row_index, words, frequency)
        col_score = sum(s.adjusted_score for s in col_choices)

        result_dict[letter] = Crosshair(
            row_score + col_score,
            [x.word for x in row_choices[-6:][::-1]],
            [x.word for x in col_choices[-6:][::-1]]
        )
    return result_dict

if __name__ == '__main__':
    words = read_words('./data/words.txt')
    frequency = read_frequencies('./make5/tiles.txt')

    while True:
        print('\nEnter your grid with commas between rows, and . for empty (eg. .....,...n.,f..a.,t..nk,....s)')
        grid = input('? ').lower().replace('.', SYMBOL).replace(' ','').split(',')
        if len(''.join(grid)) < 2:
            print('Goodbye!')
            exit()
        if len(grid[-1]) == 0:
            grid = grid[:-1]  # In case there was a trailing ,
        max_length = len(grid[0])
        min_length = 3
        print()
        print('\t\t  ' + ''.join(f'{j}' for j in range(max_length)))
        for i, row in enumerate(grid):
            print(f'\t\t{i} {row.upper()}')

        print()
        letter = input('Enter the new letter: ').lower()
        print()

        record: Dict[Tuple[int, int], Dict[str, Crosshair]] = {}
        for row_index, row_key in enumerate(grid):
            for col_index in range(len(row_key)):
                if row_key[col_index] == SYMBOL:
                    col_key = ''.join(row[col_index] for row in grid)
                    crosshair = get_crosshairs(row_key, col_key, row_index, col_index, None, words, frequency)
                    other_items = [item for item in crosshair.items() if item[0] != letter]
                    sorted_other_items = sorted(other_items, key=lambda x: x[1].score, reverse=True)

                    best_increase = crosshair[letter].score - sorted_other_items[0][1].score
                    record[(row_index, col_index)] = {
                        'crosshair': crosshair,
                        'best_increase': best_increase,
                        'best_other_letter': sorted_other_items[0][0],
                    }

        sorted_increases = sorted(record.items(), key=lambda t: t[1]['best_increase'], reverse=True)

        print('Best locations (analysing depth 1):')
        for coord, record in sorted_increases[:5]:
            print(f'{coord}: {record["best_increase"]:6.2f} {record["crosshair"][letter].score: 7.2f}  {"  ".join(record["crosshair"][letter].row)}  vs  {record["best_other_letter"]}  {"  ".join(record["crosshair"][record["best_other_letter"]].row)}')
            print(f'                        {"  ".join(record["crosshair"][letter].col)}  vs     {"  ".join(record["crosshair"][record["best_other_letter"]].col)}')

