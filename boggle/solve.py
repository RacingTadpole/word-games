"""
Run with:
    python -m boggle.solve
"""
from boggle.replacements import get_replacement_messages, restore_special
from boggle.compile_words import read_words
from typing import Sequence, Tuple, Iterator, Dict
from math import floor
from collections import Counter

from boggle.boggle_types import Position, Board

def get_all_positions(board: Board) -> Iterator[Position]:
    """
    >>> tuple(get_all_positions(['ab','cd','ef']))
    ((0, 0, 'a'), (0, 1, 'b'), (1, 0, 'c'), (1, 1, 'd'), (2, 0, 'e'), (2, 1, 'f'))
    """
    for row_number, row in enumerate(board):
        for col_number, letter in enumerate(row):
            yield (row_number, col_number, letter)

def get_unused_neighbors(board: Board, trail: Sequence[Position]) -> Iterator[Position]:
    """
    >>> trail = ((0, 1, 'a'), (1, 2, 'd'))
    >>> tuple(get_unused_neighbors(['zab','zcd','zef'], trail))
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

def find_words(board: Board, words_subtree: Dict, trail: Tuple[Position, ...] = None) -> Iterator[str]:
    """
    >>> board = ('ab','cd','ef')
    >>> words = {'b': {'a': {'d': {'.': None, 'e': {'.': None}}}}, 'a': {'c': {'e': {'.': None}}}}
    >>> tuple(find_words(board, words))
    ('ace', 'bad', 'bade')
    >>> board = ('ab','cd','fg')
    >>> tuple(find_words(board, words))
    ('bad',)
    """
    if trail is None:
        trail = ()
    if '.' in words_subtree:
        yield get_word_from_trail(trail)
    next_positions = get_all_positions(board) if len(trail) == 0 else get_unused_neighbors(board, trail)
    for next_position in next_positions:
        next_letter = next_position[2]
        if next_letter in words_subtree:
            yield from find_words(board, words_subtree[next_letter], trail + (next_position, ))

def pretty_print(words: Sequence[str], width: int = 120) -> None:
    space = max(len(word) for word in words) + 3
    num_columns = floor(width / space)
    diced_words = (words[i:i + num_columns] for i in range(0, len(words), num_columns))
    print('\n'.join(''.join(word.rjust(space) for word in sublist) for sublist in diced_words))
    print()

if __name__ == '__main__':
    # board = ["rfsem", "rante", "tsaoj", "tilft", "octhr"]
    # Eg. Enter: rfsem,rante,tsaoj,tilft,octhr
    path = './data/words.txt'
    words = read_words(path)
    replacement_messages = get_replacement_messages()
    print()
    print('\n'.join(replacement_messages))

    while True:
        board = input('\nEnter a board with commas between rows: ').lower().replace(' ','').split(',')
        board_size = len(''.join(board))
        if board_size < 2:
            print('Goodbye!')
            exit()
        min_word_length = 3 if board_size <= 20 else 4
        print()
        for row in board:
            print(f'\t\t{row.upper()}')
        found_words = tuple(word for word in find_words(board, words) if len(word) >= min_word_length)
        found_unique_words = tuple(
            restore_special(word)
            for i, word in enumerate(found_words)
            if i == 0 or word not in found_words[:i]
        )

        counts = Counter([len(word) for word in found_unique_words])
        print()
        print('  |  '.join(f'{l} letters: {count}' for l, count in sorted(counts.items())))
        print()
        if found_unique_words:
            pretty_print(found_unique_words)
            print(f'Total: {len(found_unique_words)} words\n')
        else:
            print('No words found!')
