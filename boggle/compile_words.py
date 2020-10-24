from typing import Optional
import pickle
# import json

from boggle.boggle_types import Tree

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
    next_subtree = words_subtree.get(letter, {})
    words_subtree[letter] = add_to_words_subtree(next_subtree, rest_of_word[1:])
    return words_subtree

def compile_words(path: str, outpath: str = None, words: Optional[Tree] = None) -> None:
    if outpath is None:
        stem = '.'.join(path.split('.')[:-1])
        outpath = f'{stem}-compiled.pkl'
    if words is None:
        words = {}
    with open(path, 'r') as f:
        for word_with_return in f:
            word = word_with_return.strip()
            words = add_to_words_subtree(words, word)
    # print(json.dumps(words, indent=2))

    with open(outpath, 'wb') as f:
        pickle.dump(words, f)

if __name__ == '__main__':
    # with open('./data/words-compiled.pkl', 'rb') as f:
    #     words = pickle.load(f)
    compile_words('./data/words.txt') # , words=words)
