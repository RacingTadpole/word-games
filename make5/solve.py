from typing import Dict, Tuple
from make5.crosshair import Crosshair, get_crosshairs
from make5.utilities import SYMBOL, read_frequencies
from make5.compile_words import read_words


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

