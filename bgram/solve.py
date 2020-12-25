"""
Run with:
    python -m bgram.solve
"""
import time
from bgram.compile_words import read_words
from typing import Iterable, List, Tuple, Iterator, Dict

from bgram.board import (
    Board, Direction, Point, next_point, new_board, board_with_word, gridded_board, print_board, print_grids, get_side_word)

def is_valid_word(word: str, words: Dict) -> bool:
    """
    >>> from bgram.compile_words import compile_words
    >>> is_valid_word('yoyo', compile_words())
    False
    >>> is_valid_word('egg', compile_words())
    True
    """
    if not word:
        return '.' in words
    if word[0] not in words:
        return False
    return is_valid_word(word[1:], words[word[0]])

def excise_letter(letters: Iterable[str], letter: str) -> Iterable[str]:
    """
    >>> excise_letter('abcabcd', 'a')
    'bcabcd'
    >>> excise_letter(list('abcabcd'), 'a')
    ['b', 'c', 'a', 'b', 'c', 'd']
    >>> excise_letter('abcabcd', 'b')
    'acabcd'
    >>> excise_letter('abcabcd', 'd')
    'abcabc'
    """
    index = letters.index(letter)
    return letters[:index] + letters[index + 1:]

def excise_letters(all_letters: Iterable[str], letters: str) -> Iterable[str]:
    """
    >>> excise_letters('abcabcd', 'ac')
    'babcd'
    >>> excise_letters(list('abcabcd'), 'ac')
    ['b', 'a', 'b', 'c', 'd']
    >>> excise_letters('abcabcd', 'bcdb')
    'aac'
    """
    remaining_letters = all_letters[:]
    for letter in letters:
        remaining_letters = excise_letter(remaining_letters, letter)
    return remaining_letters

def find_words(words: Dict, letters: Iterable[str], history: str = '') -> Iterator[str]:
    """
    >>> from bgram.compile_words import compile_words
    >>> sorted(find_words(compile_words(), 'fgloete'))
    ['feet', 'flee', 'fleet', 'flog']
    """
    if '.' in words:
        yield history
    for letter in set(letters):
        if letter in words:
            yield from find_words(words[letter], excise_letter(letters, letter), history + letter)

def side_words_are_valid(board: Board, start_point: Point, direction: Direction, words: Dict) -> bool:
    """
    Are all the words that cross this word valid? (Does not check the base word.)
    >>> from bgram.compile_words import compile_words
    >>> from bgram.board import Point, print_board, gridded_board
    >>> words = compile_words()
    >>> board, _ = board_with_word(new_board('fleb'), Point(2, 0), Direction.DOWN, 'egg')
    >>> side_words_are_valid(board, Point(0, 0), Direction.RIGHT, words)
    True
    >>> board, _ = board_with_word(new_board('fleb'), Point(2, 0), Direction.DOWN, 'egh')
    >>> side_words_are_valid(board, Point(0, 0), Direction.RIGHT, words)
    False
    """
    while start_point in board:
        side_word = get_side_word(board, start_point, direction)
        if side_word and not is_valid_word(side_word, words):
            return False
        start_point = next_point(start_point, direction)
    return True

# @dataclass(frozen=True)
# class BoardExtension:
#     board: Board
#     letters_used: Iterable[str]

def extended_boards(board: Board, words: Dict, banned_words: Iterable[str], letters: Iterable[str]) -> Iterator[Tuple[Board, str]]:
    """
    What new boards can we make by adding some of the new letters to the existing board?
    (without changing the existing board or extending existing words)
    >>> from bgram.compile_words import compile_words
    >>> from bgram.board import Point, print_board, gridded_board
    >>> board, _ = board_with_word(new_board('flee'), Point(2, 0), Direction.DOWN, 'egg')
    >>> print_board(board)
    FLEE
      G
      G
    >>> for board, new_letters in extended_boards(board, compile_words(), [], 'terp'):
    ...    print(new_letters, ':')
    ...    print_board(board)
    tre :
       T
       R
       E
    FLEE
      G
      G
    """
    if len(board) == 0:
        for word in find_words(words, letters):
            if word not in banned_words:
                yield new_board(word), word
    for position, existing_letter in board.items():
        for word in find_words(words, [existing_letter] + list(letters)):
            if existing_letter in word and word not in banned_words:
                for index in [i for i, l in enumerate(word) if l == existing_letter]:
                    for direction in [Direction.RIGHT, Direction.DOWN]:
                        # Do not extend from a position with a letter already on the other side.
                        # There must also be a blank space at the end of the word.
                        if (next_point(position, direction, -1) not in board and
                                next_point(position, direction, len(word) - index) not in board):
                            start_point = next_point(position, direction, -index)
                            board2, used_letters = board_with_word(board, start_point, direction, word)
                            if board2 and side_words_are_valid(board2, start_point, direction, words):
                                yield board2, used_letters

def solve_boards(board: Board, words: Dict, banned_words: Iterable[str], other_letters: Iterable[str]) -> Iterator[Board]:
    """
    >>> from bgram.compile_words import compile_words
    >>> boards = solve_boards({}, compile_words(), [], 'atlgfrgee')
    >>> grids = sorted(set(gridded_board(board) for board in boards))
    >>> print_grids(grids)
      F    TREE   T F   TREE
    T L      G    R L      G
    R A   FLAG    E A   FLAG
    EGG           EGG
    E
    <BLANKLINE>
    """
    if len(other_letters) == 0:
        yield board
    else:
        for board2, used_letters in extended_boards(board, words, banned_words, other_letters):
            if board2:
                yield from solve_boards(board2, words, banned_words, excise_letters(other_letters, used_letters))

def solve_unique_boards(words: Dict, letters: Iterable[str]) -> Iterator[Board]:
    """
    Solve for all boards, where no board can ever place any earlier board's starting word.
    This prevents duplicate boards.
    >>> from bgram.compile_words import compile_words
    >>> boards = solve_unique_boards(compile_words(), 'atlgfrgee')
    >>> len(list(boards))
    2

    The two boards are below, but it is random whether EGG is vertical or horizontal.
     TREE   TREE
       G       G
    FLAG    FLAG
    """
    banned_words: List[str] = []
    for word in find_words(words, letters):
        if word not in banned_words:
            board = new_board(word)
            banned_words.append(word)
            yield from solve_boards(board, words, banned_words, excise_letters(letters, word))

if __name__ == '__main__':
    # Eg. Enter your starting letters: rfsemrante - finds 19985 boards in 42.438 seconds.
    path = './data/words.txt'
    words = read_words(path)

    letters = input('\nEnter your starting letters: ').lower().replace(' ','')
    start = time.perf_counter()
    boards = list(solve_unique_boards(words, letters)) # Put in list to actually get them all
    grids = sorted(set(gridded_board(board) for board in boards))
    duration = time.perf_counter() - start
    print(f'Found {len(grids)} boards in {duration:.3f} seconds')
    print_grids(grids)
    if len(grids) >= 100:
        print(f'Found {len(grids)} boards in {duration:.3f} seconds')
