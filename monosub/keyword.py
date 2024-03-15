from ciphers.analysis import (
    ALPHABET,
    CUTOFF_TETRA_FITNESS,
    WORDS_FP,
    get_freq,
    read_dict,
    tetra_fitness,
)
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
    key += ALPHABET[i:] + ALPHABET[:i]
    return remove_duplicates(key)


def fill_key_3(word):
    key = remove_duplicates(word)
    i = ALPHABET.index(sorted(word)[-1])
    key += ALPHABET[i:] + ALPHABET[:i]
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
        case 5:
            key = fill_key_5(keyword)
        case _:
            raise ValueError("Not a valid method to fill an alphabet key")
    if invert:
        key = invert_key(key)
    return "".join(key)


def encipher_keyword(plaintext, keyword, method=1):
    key = generate_alphabet_keyword(keyword, method)
    return encipher_mono_sub(plaintext, key)


def decipher_keyword(ciphertext, keyword, method=1):
    key = generate_alphabet_keyword(keyword, method)
    return decipher_mono_sub(ciphertext, key)


def output_keyword(ciphertext, keyword, method):
    key = generate_alphabet_keyword(keyword, method)
    plaintext = decipher_mono_sub(ciphertext, key)
    print("Keyword:", keyword)
    print(f"Key (method={method}: {key}")
    print("Plaintext:", plaintext)


def dictionary_keyword(ciphertext):
    words = read_dict(WORDS_FP).keys()
    expected = get_freq(4)
    found = False
    for word, method in ((x, y) for x in words for y in range(1, 4)):
        poss_text = decipher_keyword(ciphertext, word, method)
        fitness = tetra_fitness(poss_text, expected)
        if fitness > CUTOFF_TETRA_FITNESS:
            found = True
            break
    if found:
        output_keyword(ciphertext, word, method)
    else:
        print("Dictionary attack failed")
