from make5.types import FrequencyDict, WordDict
from make5.utilities import SYMBOL
from typing import Dict, Tuple, List
from make5.crosshair import Crosshair, get_crosshairs


def calculate(grid: List[str], letter: str, words: WordDict, frequency: FrequencyDict) -> Dict[Tuple[int, int], Dict[str, Crosshair]]:
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

    return record
