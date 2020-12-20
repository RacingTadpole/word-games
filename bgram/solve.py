"""
Run with:
    python -m bgram.solve
"""
from bgram.compile_words import read_words
from typing import Iterable, Tuple, Iterator, Dict

from bgram.board import Board, Direction, next_point, new_board, board_with_word, gridded_board, print_grids


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

def extended_boards(board: Board, words: Dict, letters: Iterable[str]) -> Iterator[Tuple[Board, str]]:
    """
    What new boards can we make by adding some of the new letters to the existing board?
    (without changing the existing board or extending existing words)
    >>> from bgram.compile_words import compile_words
    >>> from bgram.board import Point, print_board, gridded_board
    >>> board = board_with_word(new_board('flee'), Point(2, 0), Direction.DOWN, 'egg')
    >>> print_board(board)
    FLEE
      G 
      G 
    >>> for board, new_letters in extended_boards(board, compile_words(), 'terp'):
    ...    print(new_letters, ':')
    ...    print_board(board)
    tre :
       T
       R
    FLEE
      GE
      G 
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
            yield new_board(word), word
    for position, existing_letter in board.items():
        for word in find_words(words, [existing_letter] + list(letters)):
            if existing_letter in word:
                for index in [i for i, l in enumerate(word) if l == existing_letter]:
                    for direction in [Direction.RIGHT, Direction.DOWN]:
                        # Do not extend from a position with a letter already on the other side.
                        if next_point(position, direction, -1) not in board:
                            board2 = board_with_word(board, next_point(position, direction, -index), direction, word)
                            if board2:
                                # There must be a blank space at the end of the word.
                                if next_point(position, direction, len(word) - index) not in board2:
                                    yield board2, excise_letter(word, existing_letter)

def solve_boards(board: Board, words: Dict, other_letters: Iterable[str]) -> Iterator[Board]:
    """
    >>> from bgram.compile_words import compile_words
    >>> boards = solve_boards({}, compile_words(), 'atlgfrgee')
    >>> grids = sorted(set(gridded_board(board) for board in boards))
    >>> print_grids(grids)
       F     F     F      T       T      F     TREE    TREE   T F   TF    TREE   TREE
       L   T L     L      R       R     TL       G    FLAG    R L   RL       G   FLAG
    TREE   R A   TREE     EGG   FLEA    RA    FLAG       G    E A   EA    FLAG      G
      GA   EGG     AG   FLEA      EGG   EGG                   EGG   EGG              
      G    E        G                   E                                            
    <BLANKLINE>
    """
    if len(other_letters) == 0:
        yield board
    else:
        for board2, word in extended_boards(board, words, other_letters):
            yield from solve_boards(board2, words, excise_letters(other_letters, word))

if __name__ == '__main__':
    # Eg. Enter your starting letters: rfsemrantetsaojtilfto
    path = './data/words.txt'
    words = read_words(path)

    letters = input('\nEnter your starting letters: ').lower().replace(' ','')
    boards = solve_boards({}, words, letters)
    grids = sorted(set(gridded_board(board) for board in boards))
    print(f'Found {len(grids)} boards')
    print_grids(grids)