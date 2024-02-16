from ciphers.analysis import ALPHABET
from ciphers.monosub.mono_sub import decipher_mono_sub, encipher_mono_sub, invert_key


def remove_duplicates(items):
    new_items = []
    for element in items:
        if element not in new_items:
            new_items.append(element)
    return new_items


def fill_key_1(word):
    key = word + ALPHABET
    return remove_duplicates(key)


def fill_key_2(word):
    key = remove_duplicates(word)
    i = ALPHABET.index(word[-1])
    key.extend(ALPHABET[i:])
    key.extend(ALPHABET[:i])
    return remove_duplicates(key)


def fill_key_3(word):
    key = remove_duplicates(word)
    i = ALPHABET.index(sorted(word)[-1])
    key.extend(ALPHABET[i:])
    key.extend(ALPHABET[:i])
    return remove_duplicates(key)


def fill_key_4(word):
    key = word + ALPHABET[::-1]
    return remove_duplicates(key)


def fill_key_5(word):
    key = ALPHABET + word
    return remove_duplicates(key)


def generate_alphabet_keyword(keyword, method, invert=False):
    match method:
        case 1:
            key = fill_key_1(keyword)
        case 2:
            key = fill_key_2(keyword)
        case 3:
            key = fill_key_3(keyword)
        case 4:
            key = fill_key_4(keyword)
        case _:
            raise ValueError("Not a valid method to fill an alphabet key")
    if invert:
        key = invert_key(key)
    return "".join(key)


def encipher_keyword(plaintext, keyword, method=1):
    key = generate_alphabet_keyword(keyword, method)
    return encipher_mono_sub(plaintext, key)


def decipher_keyword(plaintext, keyword, method=1):
    key = generate_alphabet_keyword(keyword, method)
    return decipher_mono_sub(plaintext, key)
