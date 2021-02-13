from typing import List


def replace_special(word: str) -> str:
    return word.replace('qu', '≈').replace('q', '√').replace('≈', 'q')

def restore_special(replaced_word: str) -> str:
    return replaced_word.replace('q', 'qu').replace('√', 'q')

def get_replacement_messages() -> List[str]:
    return [
        "Note: If there's a 'Qu' in your board, just type Q.",
        # (To get just a Q, you need to type √) TODO: doesn't work.
    ]
