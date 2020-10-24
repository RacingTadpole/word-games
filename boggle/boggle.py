"""
Run with:
    python -m boggle.boggle
"""
from typing import Iterable, Sequence, Tuple
import pickle

from boggle.boggle_types import Tree, Position, Board

def get_all_positions(board: Board) -> Sequence[Position]:
    """
    >>> tuple(get_all_positions(['ab','cd','ef']))
    ((0, 0, 'a'), (0, 1, 'b'), (1, 0, 'c'), (1, 1, 'd'), (2, 0, 'e'), (2, 1, 'f'))
    """
    for row_number, row in enumerate(board):
        for col_number, letter in enumerate(row):
            yield (row_number, col_number, letter)

def get_unused_neighbours(board: Board, trail: Sequence[Position]) -> Iterable[Position]:
    """
    >>> trail = ((0, 1, 'a'), (1, 2, 'd'))
    >>> tuple(get_unused_neighbours(['zab','zcd','zef'], trail))
    ((1, 1, 'c'), (2, 1, 'e'), (0, 2, 'b'), (2, 2, 'f'))
    """
    last = trail[-1]
    for across_move in (-1, 0, 1):
        for up_down_move in (-1, 0, 1):
            row_number = last[0] + up_down_move
            col_number = last[1] + across_move
            if row_number < 0 or row_number >= len(board) or col_number < 0 or col_number >= len(board[row_number]):
                continue
            position = (row_number, col_number, board[row_number][col_number])
            if position not in trail:
                yield position

def get_word_from_trail(trail: Tuple[Position, ...]) -> str:
    """
    >>> trail = ((1, 0, 'b'), (0, 1, 'a'), (1, 2, 'd'))
    >>> get_word_from_trail(trail)
    'bad'
    """
    return ''.join(position[2] for position in trail)

def find_words(board: Board, words_subtree: Tree, trail: Tuple[Position, ...] = None) -> Sequence[str]:
    """
    >>> board = ('ab','cd','ef')
    >>> words = {'b': {'a': {'d': {'.': None, 'e': {'.': None}}}}, 'a': {'c': {'e': {'.': None}}}}
    >>> tuple(find_words(board, words))
    ('ace', 'bad', 'bade')
    """
    if trail is None:
        trail = ()
    if '.' in words_subtree:
        yield get_word_from_trail(trail)
    next_positions = get_all_positions(board) if len(trail) == 0 else get_unused_neighbours(board, trail)
    for next_position in next_positions:
        next_letter = next_position[2]
        if next_letter in words_subtree:
            yield from find_words(board, words_subtree[next_letter], trail + (next_position, ))

if __name__ == '__main__':
    # board = ["rfsem", "rfsem", "tsaoj", "tilft", "octhr"]
    # Eg. Enter: rfsem,rfsem,tsaoj,tilft,octhr
    board = input('Enter a board with commas between rows: ').lower().split(',')
    with open('./data/words-compiled.pkl', 'rb') as f:
        words = pickle.load(f)
    found_words = tuple(word for word in find_words(board, words) if len(word) >= 4)
    found_unique_words = tuple(word for i, word in enumerate(found_words) if i == 0 or word not in found_words[:i])
    print('\n'.join(found_unique_words))
    number = len(found_unique_words)
    print(f'\nFound {number} different words\n')
