from collections import Counter

from ciphers.analysis import (
    get_freq,
    mono_frequencies,
    plot_dict,
    split_into_ngrams,
    split_into_slices,
)
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
    return num_to_letter(output)


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


def get_signature(text):
    return list(mono_frequencies(text).values())


def twist(a, b):
    return sum([x - y if i <= 12 else x + y for i, (x, y) in enumerate(zip(a, b))])


def find_period_twist(ciphertext):
    twists = {}
    for i in range(2, 20):
        signatures = []
        slices = split_into_slices(ciphertext, i)
        for s in slices:
            signatures.append(get_signature(s))
        signature = [sum(vs) / len(vs) for vs in zip(*signatures)]
        expected = get_freq(1)
        twists[i] = twist(signature, expected.values())
    plot_dict(twists)
    return max(twists, key=twists.get)
