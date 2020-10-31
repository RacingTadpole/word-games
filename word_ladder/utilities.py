def get_word_with_letter_missing(word: str, position: int) -> str:
    """
    >>> get_word_with_letter_missing('dog', 0)
    '?og'
    >>> get_word_with_letter_missing('dog', 1)
    'd?g'
    >>> get_word_with_letter_missing('dog', 2)
    'do?'
    """
    if position == 0:
        return f'?{word[1:]}'
    if position == len(word) - 1:
        return f'{word[:-1]}?'
    return f'{word[:position]}?{word[position + 1:]}'
