from make5.types import FrequencyDict, WordDict
from make5.utilities import SYMBOL
from typing import Any, Dict, Tuple, List
from make5.crosshair import Crosshair, get_crosshairs


def calculate(grid: List[str], letter: str, words: WordDict, frequency: FrequencyDict) -> Dict[Tuple[int, int], Dict[str, Any]]:
    record: Dict[Tuple[int, int], Dict[str, Any]] = {}
    for row_index, row_key in enumerate(grid):
        for col_index in range(len(row_key)):
            if row_key[col_index] == SYMBOL:
                col_key = ''.join(row[col_index] for row in grid)
                crosshairs = get_crosshairs(row_key, col_key, row_index, col_index, None, words, frequency)
                this_crosshair = [crosshair for crosshair in crosshairs if crosshair.letter == letter][0]
                other_crosshairs = [crosshair for crosshair in crosshairs if crosshair.letter != letter]
                sorted_other_crosshairs = sorted(other_crosshairs, key=lambda x: x.score, reverse=True)
                # for new_letter, new_crosshair in sorted_other_crosshairs[:3]:

                best_increase = this_crosshair.score - sorted_other_crosshairs[1].score
                record[(row_index, col_index)] = {
                    'crosshair': this_crosshair,
                    'best_increase': best_increase,
                    'best_other_crosshair': sorted_other_crosshairs[0],
                }

    return record
