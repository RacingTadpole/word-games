from typing import Dict, Iterable, Iterator, Optional, Sequence, Tuple
from dataclasses import dataclass
from enum import Enum
from math import floor

class Direction(Enum):
    RIGHT = 1
    DOWN = 2

side_direction = {
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.RIGHT,
}

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

def side_points(point: Point, direction: Direction) -> Iterator[Point]:
    """
    Yield the two points on either side of the current point,
    when facing the given direction.
    >>> tuple(side_points(Point(3, -1), Direction.RIGHT))
    (Point(x=3, y=-2), Point(x=3, y=0))
    >>> tuple(side_points(Point(3, -1), Direction.DOWN))
    (Point(x=2, y=-1), Point(x=4, y=-1))
    """
    yield next_point(point, side_direction[direction], -1)
    yield next_point(point, side_direction[direction], 1)

Board = Dict[Point, str]
Grid = Sequence[Sequence[str]]

def get_word_start(board: Board, point: Point, direction: Direction) -> Point:
    """
    >>> board, _ = board_with_word(new_board('flea'), Point(2, 0), Direction.DOWN, 'egg')
    >>> get_word_start(board, Point(2, 0), Direction.RIGHT)
    Point(x=0, y=0)
    >>> get_word_start(board, Point(2, 2), Direction.DOWN)
    Point(x=2, y=0)
    >>> get_word_start(board, Point(2, 0), Direction.DOWN)
    Point(x=2, y=0)
    >>> get_word_start(board, Point(9, 9), Direction.DOWN)
    Point(x=9, y=9)
    """
    last_point = point
    while point in board:
        last_point = point
        point = next_point(point, direction, -1)
    return last_point

def get_letters(board: Board, start_point: Point, direction: Direction) -> Iterator[str]:
    """
    Yield the letters of the word that starts at this point in the given direction.
    >>> board, _ = board_with_word(new_board('flea'), Point(2, 0), Direction.DOWN, 'egg')
    >>> ''.join(get_letters(board, Point(2, 0), Direction.DOWN))
    'egg'
    >>> ''.join(get_letters(board, Point(2, 0), Direction.RIGHT))
    'ea'
    """
    while start_point in board:
        yield board[start_point]
        start_point = next_point(start_point, direction)

def get_side_word(board: Board, point: Point, direction: Direction) -> Optional[str]:
    """
    At the given point, facing in the given direction, see if there's a crossways word.
    >>> board, _ = board_with_word(new_board('flea'), Point(2, 0), Direction.DOWN, 'egg')
    >>> get_side_word(board, Point(2, 0), Direction.RIGHT)
    'egg'
    >>> board, _ = board_with_word(new_board('flea'), Point(3, -1), Direction.DOWN, 'path')
    >>> get_side_word(board, Point(3, 0), Direction.RIGHT)
    'path'
    >>> board, _ = board_with_word(new_board('flea'), Point(1, -3), Direction.DOWN, 'pill')
    >>> get_side_word(board, Point(1, 0), Direction.RIGHT)
    'pill'
    >>> get_side_word(board, Point(2, 0), Direction.RIGHT)
    """
    if any(side_point in board for side_point in side_points(point, direction)):
        start_point = get_word_start(board, point, side_direction[direction])
        return ''.join(get_letters(board, start_point, side_direction[direction]))
    return None

def gridded_board(board: Board) -> Grid:
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
    print('\n'.join([''.join(x).rstrip() for x in gridded_board(board)]))

def print_grids(grids: Sequence[Grid], width: int = 120, padding: int = 3) -> None:
    """
    >>> board = {Point(x=0, y=0): 'b', Point(x=0, y=1): 'a', Point(x=0, y=2): 'r', Point(x=1, y=1): 'x'}
    >>> board2 = {Point(x=0, y=0): 'b', Point(x=1, y=0): 'a', Point(x=2, y=0): 'r'}
    >>> grid, grid2 = gridded_board(board), gridded_board(board2)
    >>> print_grids([grid, grid, grid, grid2, grid])
    B    B    B    BAR   B
    AX   AX   AX         AX
    R    R    R          R
    <BLANKLINE>
    >>> print_grids([grid, grid, grid, grid2, grid], 21)
    B    B    B
    AX   AX   AX
    R    R    R
    <BLANKLINE>
    BAR   B
          AX
          R
    <BLANKLINE>
    """
    if not grids:
        return
    max_width = max(len(grid) for grid in grids)
    num = floor(width / (max_width + padding))
    diced_grids = (grids[i:i + num] for i in range(0, len(grids), num))
    rows = []
    for row_of_grids in diced_grids:
        for i in range(max(len(grid) for grid in row_of_grids)):
            rows += [(' ' * padding).join(''.join(x for x in (grid[i] if len(grid) > i else ' ' * len(grid[0]))) for grid in row_of_grids).rstrip()]
        rows += ['']
    print('\n'.join(rows))

def place_word(board: Board, where: Point, direction: Direction, word: str, placed_so_far: str) -> Iterable[str]:
    """
    Mutates board. Returns the letters that are placed (ie. skipping any already on the board).
    Only for internal use.
    >>> board = {}
    >>> place_word(board, Point(0, 0), Direction.DOWN, 'bar', '')
    'bar'
    >>> board
    {Point(x=0, y=0): 'b', Point(x=0, y=1): 'a', Point(x=0, y=2): 'r'}
    >>> place_word(board, Point(0, 1), Direction.RIGHT, 'ax', '')
    'x'
    >>> board
    {Point(x=0, y=0): 'b', Point(x=0, y=1): 'a', Point(x=0, y=2): 'r', Point(x=1, y=1): 'x'}
    >>> import pytest
    >>> with pytest.raises(Exception):
    ...     place_word(board, Point(0, 0), Direction.RIGHT, 'zoo')
    """
    if not word:
        return placed_so_far
    letter = word[0]
    if where in board:
        if board[where] != letter:
            raise Exception(f'Inconsistent letters {letter} and {board[where]} at {where}.')
    else:
        board.update({where: letter})
        placed_so_far = placed_so_far + letter
    return place_word(board, next_point(where, direction), direction, word[1:], placed_so_far)

def board_with_word(board: Board, where: Point, direction: Direction, word: str) -> Tuple[Optional[Board], str]:
    """
    Does not mutate the board. Returns None if the word cannot be placed.
    Does not check that any ancillary words formed are true words.
    >>> board = new_board('bar')
    >>> board2, used = board_with_word(board, Point(1, 0), Direction.DOWN, 'ax')
    >>> assert len(board) == 3
    >>> assert len(board2) == 4
    >>> used
    'x'
    >>> board_with_word(board, Point(1, -1), Direction.DOWN, 'foo')[0] # already an "a" in the way.
    >>> board_with_word(board, Point(0, 0), Direction.RIGHT, 'bar')[0] # No new letters placed.
    """
    board2 = dict(board)
    letters_used = ''
    try:
        letters_used = place_word(board2, where, direction, word, '')
    except:
        return None, ''
    return (board2 if letters_used else None), letters_used

def new_board(first_word: str, direction: Direction=Direction.RIGHT) -> Board:
    """
    >>> new_board('up')
    {Point(x=0, y=0): 'u', Point(x=1, y=0): 'p'}
    """
    board = {}
    place_word(board, Point(0, 0), direction, first_word, '')
    return board
