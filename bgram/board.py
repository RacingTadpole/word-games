from typing import Dict, Iterable, Optional, List, Sequence
from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    RIGHT = 1
    DOWN = 2

@dataclass(frozen=True)
class Point:
    x: int
    y: int

def next_point(point: Point, direction: Direction, step: int = 1) -> Point:
    """
    >>> next_point(Point(3, -1), Direction.RIGHT)
    Point(x=4, y=-1)
    >>> next_point(Point(3, -1), Direction.DOWN)
    Point(x=3, y=0)
    >>> next_point(Point(3, -1), Direction.DOWN, -1)
    Point(x=3, y=-2)
    """
    if direction == Direction.RIGHT:
        return Point(point.x + step, point.y)
    if direction == Direction.DOWN:
        return Point(point.x, point.y + step)

Board = Dict[Point, str]

def gridded_board(board: Board) -> Sequence[Sequence[str]]:
    """
    >>> board = {Point(x=0, y=0): 'b', Point(x=0, y=1): 'a', Point(x=0, y=2): 'r', Point(x=1, y=1): 'x'}
    >>> gridded_board(board)
    (('B', ' '), ('A', 'X'), ('R', ' '))
    """
    min_x, min_y = min(p.x for p in board), min(p.y for p in board)
    max_x, max_y = max(p.x for p in board), max(p.y for p in board)
    return tuple(
        tuple(board.get(Point(x, y), ' ').upper() for x in range(min_x, max_x + 1))
        for y in range(min_y, max_y + 1)
        )

def print_board(board: Board) -> None:
    """
    >>> board = {Point(x=0, y=0): 'b', Point(x=0, y=1): 'a', Point(x=0, y=2): 'r', Point(x=1, y=1): 'x'}
    >>> print_board(board)
    B 
    AX
    R 
    """
    print('\n'.join([''.join(x) for x in gridded_board(board)]))

def place_word(board: Board, where: Point, direction: Direction, word: str):
    """
    Mutates board. Only for internal use.
    >>> board = {}
    >>> place_word(board, Point(0, 0), Direction.DOWN, 'bar')
    >>> board
    {Point(x=0, y=0): 'b', Point(x=0, y=1): 'a', Point(x=0, y=2): 'r'}
    >>> place_word(board, Point(0, 1), Direction.RIGHT, 'ax')
    >>> board
    {Point(x=0, y=0): 'b', Point(x=0, y=1): 'a', Point(x=0, y=2): 'r', Point(x=1, y=1): 'x'}
    >>> import pytest
    >>> with pytest.raises(Exception):
    ...     place_word(board, Point(0, 0), Direction.RIGHT, 'zoo')
    """
    if not word:
        return board
    letter = word[0]
    if board.get(where, letter) != letter:
        raise Exception(f'Inconsistent letters {letter} and {board[where]} at {where}.')
    board.update({where: letter})
    place_word(board, next_point(where, direction), direction, word[1:])

def board_with_word(board: Board, where: Point, direction: Direction, word: str) -> Optional[Board]:
    """
    Does not mutate the board. Returns None if the word cannot be placed.
    >>> board = new_board('bar')
    >>> board2 = board_with_word(board, Point(1, 0), Direction.DOWN, 'ax')
    >>> assert len(board) == 3
    >>> assert len(board2) == 4
    """
    board2 = dict(board)
    try:
        place_word(board2, where, direction, word)
    except:
        return None
    # TODO: check spelling of any new words formed.
    return board2

def new_board(first_word: str, direction: Direction=Direction.RIGHT) -> Board:
    """
    >>> new_board('up')
    {Point(x=0, y=0): 'u', Point(x=1, y=0): 'p'}
    """
    board = {}
    place_word(board, Point(0, 0), direction, first_word)
    return board
