from dataclasses import dataclass
from make5.types import FrequencyDict, WordDict
from typing import Dict, Optional, Sequence
from make5.choice import get_sorted_choices
from make5.utilities import replace

ALL_LETTERS = 'abcdefghijklmnopqrstuvwxyz'


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
    >>> from .utilities import _get_test_words, read_frequencies
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