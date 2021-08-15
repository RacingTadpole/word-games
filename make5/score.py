MAX_LENGTH_BONUS = 5


def get_score(word: str, max_length: int = 5) -> int:
    return len(word) + (MAX_LENGTH_BONUS if len(word) == max_length else 0)
