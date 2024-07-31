from collections import Counter
from copy import deepcopy
from random import shuffle

from ciphers.analysis import (
    ALPHABET,
    get_freq,
    mono_frequencies,
    plot_dict,
    split_into_ngrams,
    split_into_slices,
    tetra_fitness,
)
from ciphers.monosub import (
    decipher_mono_sub,
    gcd,
    letter_to_num,
    num_to_letter,
    swap_random,
)
from ciphers.polysub.vigenere import get_period


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


def output_polysub(ciphertext, keys):
    plaintext = decipher_poly_sub(ciphertext, keys)
    print("Keys:")
    print("\n".join(keys))
    print("Plaintext:", plaintext)


def find_all(s, substring):
    return [i for i in range(len(s)) if s.startswith(substring, i)]


def find_period_repeats(ciphertext):
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
    expected = get_freq(1).values()
    for i in range(2, 10):
        signatures = []
        slices = split_into_slices(ciphertext, i)
        for s in slices:
            signatures.append(get_signature(s))
        signature = [sum(vs) / len(vs) for vs in zip(*signatures)]
        twists[i] = twist(signature, expected)
    plot_dict(twists)
    return max(twists, key=twists.get)


def hill_climbing_poly_sub(ciphertext, period=None):
    if period is None:
        period = get_period(ciphertext)
    big_counter = 0
    expected = get_freq(4)
    best_fitness = tetra_fitness(ciphertext, expected)
    parent_key = [list(ALPHABET) for _ in range(period)]
    while big_counter < 10e6 * period**2:
        for i in range(period):
            current = parent_key[i]
            shuffle(current)
            parent_key[i] = current
            plaintext_attempt = decipher_poly_sub(ciphertext, parent_key)
            parent_fitness = tetra_fitness(plaintext_attempt, expected)
            little_counter = 0
            while little_counter < 1000:
                child_key = deepcopy(parent_key)
                child_key[i] = swap_random(child_key[i])
                plaintext_attempt = decipher_poly_sub(ciphertext, child_key)
                child_fitness = tetra_fitness(plaintext_attempt, expected)
                if child_fitness > parent_fitness:
                    parent_key = deepcopy(child_key)
                    parent_fitness = child_fitness
                    little_counter = 0
                little_counter += 1
                print(little_counter)
        if child_fitness > best_fitness:
            best_fitness = child_fitness
            best_key = deepcopy(child_key)
            big_counter = 0
        big_counter += 1
        print(f"{big_counter=}")
    best_key = ["".join(key) for key in best_key]
    output_polysub(ciphertext, best_key)
