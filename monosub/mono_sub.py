from ciphers.analysis import (
    ALPHABET,
    ioc,
    mono_fitness,
    get_freq,
)


def mono_sub_likely(ciphertext):
    expected = get_freq(1)
    similar_ioc = abs(ioc(ciphertext) - 1.73) < 0.2
    low_mono_fitness = abs(mono_fitness(ciphertext, expected) - 0.96) > 0.2
    return similar_ioc and low_mono_fitness


def invert_key(key):
    indexes = [key.index(letter) for letter in ALPHABET]
    return [ALPHABET[index] for index in indexes]


def encipher_mono_sub(plaintext, key):
    if isinstance(key, list):
        key = "".join(key)
    table = str.maketrans(ALPHABET, key)
    return plaintext.translate(table)


def decipher_mono_sub(ciphertext, key):
    return encipher_mono_sub(ciphertext, invert_key(key))


def atbash(text):
    key = ALPHABET[::-1]
    return encipher_mono_sub(text, key)


def albam(text):
    key = ALPHABET[13:] + ALPHABET[:13]
    return encipher_mono_sub(text, key)
