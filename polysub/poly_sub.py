from collections import Counter

from ciphers.analysis import split_into_ngrams
from ciphers.monosub import (
    decipher_mono_sub,
    gcd,
    letter_to_num,
    num_to_letter,
)


def encipher_poly_sub(plaintext, keys):
    plaintext = letter_to_num(plaintext)
    keys = [letter_to_num(key) for key in keys]
    output = []
    for i, letter in enumerate(plaintext):
        i %= len(keys)
        key = keys[i]
        output.append(key[letter])
    output = num_to_letter(output)
    return "".join(output)


def decipher_poly_sub(ciphertext, keys):
    output = []
    for i, letter in enumerate(ciphertext):
        i %= len(keys)
        key = keys[i]
        output.append(decipher_mono_sub(letter, key))
    return "".join(output)


def find_all(s, substring):
    return [i for i in range(len(s)) if s.startswith(substring, i)]


def find_period(ciphertext):
    differences = []
    for n in range(10, 5, -1):
        ngrams = Counter(split_into_ngrams(ciphertext, n))
        ngrams = {ngram: count for ngram, count in ngrams.items() if count > 1}
        for ngram, count in ngrams.items():
            indexes = find_all(ciphertext, ngram)
            for i in range(count - 1):
                differences.append(indexes[i + 1] - indexes[i])
    if len(differences) < 2:
        raise ValueError("No repeat occurences")
    return gcd(*differences)
