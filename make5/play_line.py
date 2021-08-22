from make5.choice import get_sorted_choices, print_choices
from make5.utilities import SYMBOL, read_frequencies
from make5.compile_words import read_words


if __name__ == '__main__':
    words = read_words('./data/words.txt')
    frequency = read_frequencies('./make5/tiles.txt')

    while True:
        print()
        key = input('Enter an expression, eg. ".re..": ')
        key = key.replace('.', SYMBOL)
        if not key:
            print('Goodbye!')
            exit()
        letter = input('Enter the new letter (if any): ')
        print()

        if letter:
            for position in range(len(key)):
                if key[position] == SYMBOL:
                    this_key = ''.join(letter if i == position else key[i] for i in range(len(key)))
                    print(this_key)
                    print_choices(get_sorted_choices(this_key, position, words, frequency))
        else:
            print_choices(get_sorted_choices(key, None, words, frequency))
