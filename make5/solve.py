from make5.calculate import calculate
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

        record = calculate(grid, letter, words, frequency)
        sorted_increases = sorted(record.items(), key=lambda t: t[1]['best_increase'], reverse=True)

        print('Best locations (analysing depth 1):')
        for coord, record in sorted_increases[:5]:
            print(f'{coord}: {record["best_increase"]:6.2f} {record["crosshair"][letter].score: 7.2f}  {"  ".join(record["crosshair"][letter].row)}  vs  {record["best_other_letter"]}  {"  ".join(record["crosshair"][record["best_other_letter"]].row)}')
            print(f'                        {"  ".join(record["crosshair"][letter].col)}  vs     {"  ".join(record["crosshair"][record["best_other_letter"]].col)}')

