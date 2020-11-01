from typing import Dict, Iterable, Iterator, List, Sequence, Optional, Tuple
from word_ladder.types import WordDict
from word_ladder.rung import Rung


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


def get_neighbors(word: str, words: WordDict) -> Sequence[str]:
    """
    >>> words = {'?og': ['dog', 'log', 'fog'], 'd?g': ['dog', 'dig'], 'do?': ['dog'], 'l?g': ['log'], 'lo?': ['log']}
    >>> sorted(get_neighbors('dig', words))
    ['dig', 'dog']
    >>> sorted(get_neighbors('fog', words))
    ['dog', 'fog', 'log']
    """
    return frozenset(
        neighbor
        for position in range(len(word))
        for neighbor in words.get(get_word_with_letter_missing(word, position), [])
    )

def get_all_previous_words(rung: Rung) -> Tuple[str]:
    """
    >>> rung_0 = Rung(None, ['dig'], {})
    >>> path = {'dog': ('log', 'fog', 'dig', 'dug', 'don', 'dob'), 'fig': ('dig', 'fog', 'fin')}
    >>> words = ['dob', 'don', 'dug', 'fin', 'fog', 'log']
    >>> rung_1 = Rung(rung_0, words, path)
    >>> sorted(get_all_previous_words(rung_1))
    ['dig', 'dob', 'don', 'dug', 'fin', 'fog', 'log']
    """
    return tuple(rung.words) + (get_all_previous_words(rung.previous) if rung.previous else ())

def get_next_rung(previous_rung: Rung, words: WordDict) -> Rung:
    """
    >>> from word_ladder.compile_words import add_to_words_dict
    >>> words = {}
    >>> for w in ['dog', 'log', 'fog', 'dig', 'dug', 'dim', 'don', 'dob', 'lug', 'fin']:
    ...     words = add_to_words_dict(words, w)
    >>> rung = Rung(None, ['dog', 'fig'], {})
    >>> next_rung = get_next_rung(rung, words)
    >>> {k: sorted(v) for k,v in next_rung.path.items()}
    {'dog': ['dig', 'dob', 'don', 'dug', 'fog', 'log'], 'fig': ['dig', 'fin', 'fog']}
    >>> sorted(next_rung.words)
    ['dig', 'dob', 'don', 'dug', 'fin', 'fog', 'log']
    """
    previous_words = get_all_previous_words(previous_rung)
    path = {
        source_word: tuple(w for w in get_neighbors(source_word, words) if w not in previous_words)
        for source_word in previous_rung.words
    }
    word_soup = frozenset(w for these_words in path.values() for w in these_words)
    return Rung(previous_rung, word_soup, path)

def keys_for_value(d: Dict[str, Iterable[str]], value: str) -> Iterator[str]:
    """
    >>> d = {'a': ['x', 'y', 'z'], 'b': ['l', 'm', 'z'], 'c': ['t', 'u']}
    >>> list(keys_for_value(d, 'y'))
    ['a']
    >>> list(keys_for_value(d, 'u'))
    ['c']
    >>> list(keys_for_value(d, 'z'))
    ['a', 'b']
    """
    for key, values in d.items():
        if value in values:
            yield key

def get_ladders(rung: Rung, word: str) -> Sequence[List[str]]:
    """
    >>> rung_0 = Rung(None, ['dig'], {})
    >>> rung_1 = Rung(rung_0, ['dog', 'log', 'fig', 'din'], {'dig': ('dog', 'log', 'fig', 'din')})
    >>> words = ['dig', 'dob', 'don', 'dug', 'fin', 'fog', 'log', 'din']
    >>> path = {'dog': ('log', 'fog', 'dig', 'dug', 'don', 'dob'), 'fig': ('dig', 'fog', 'fin'), 'din': ('dig', 'fin')}
    >>> rung_2 = Rung(rung_1, words, path)
    >>> get_ladders(rung_2, 'fin')
    [['dig', 'fig', 'fin'], ['dig', 'din', 'fin']]
    """
    if not rung.previous:
        return [[word]]
    return [
        ladder + [word]
        for previous_word in keys_for_value(rung.path, word)
        for ladder in get_ladders(rung.previous, previous_word)
    ]

def build_rungs(start_word, target_word, words) -> Rung:
    rung = Rung(None, [start_word], {})
    counter = 1
    while target_word not in rung.words and len(rung.words) > 0:
        rung = get_next_rung(rung, words)
        counter += 1
        if rung.words:
            print(f'Round {counter}: {len(rung.words):3} possible words, eg. {", ".join(sorted(rung.words)[:6])}')
    return rung
