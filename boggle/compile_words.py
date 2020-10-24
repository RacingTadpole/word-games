from typing import Dict, Any, Optional
from copy import deepcopy
import pickle
# import json

Tree = Dict[str, Any]

def add_to_words_subtree(words_subtree: Tree, rest_of_word: str) -> Tree:
    """
    >>> add_to_words_subtree({}, 'b')
    {'b': {'.': None}}
    >>> add_to_words_subtree({}, 'bar')
    {'b': {'a': {'r': {'.': None}}}}
    >>> add_to_words_subtree({'r': {'.': None}}, 'n')
    {'r': {'.': None}, 'n': {'.': None}}
    >>> add_to_words_subtree({'r': {'.': None}}, 'ns')
    {'r': {'.': None}, 'n': {'s': {'.': None}}}
    >>> add_to_words_subtree({'b': {'a': {'r': {'.': None}}}}, 'be')
    {'b': {'a': {'r': {'.': None}}, 'e': {'.': None}}}
    >>> add_to_words_subtree({'b': {'a': {'r': {'.': None}}}}, 'am')
    {'b': {'a': {'r': {'.': None}}}, 'a': {'m': {'.': None}}}
    """
    if len(rest_of_word) == 0:
        return {'.': None}
    letter = rest_of_word[0]
    subtree_copy = deepcopy(words_subtree)
    subtree_copy[letter] = add_to_words_subtree(words_subtree.get(letter, {}), rest_of_word[1:])
    return subtree_copy

def compile_words(path: str, outpath: str = None, words: Optional[Tree] = None) -> None:
    if outpath is None:
        stem = '.'.join(path.split('.')[:-1])
        outpath = f'{stem}-compiled.pkl'
    if words is None:
        words = {}
    with open(path, 'r') as f:
        for word in f:
            words = add_to_words_subtree(words, word)
    # print(json.dumps(words, indent=2))

    with open(outpath, 'wb') as f:
        pickle.dump(words, f)

if __name__ == '__main__':
    compile_words('./data/short-words.txt')
