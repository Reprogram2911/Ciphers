from random import sample

import numpy as np

from ciphers.analysis import (
    ALPHABET,
    CUTOFF_TETRA_FITNESS,
    EXPECTED_MONO_FITNESS,
    get_freq,
    mono_fitness,
    similar_ioc,
    tetra_fitness,
)


def mono_sub_likely(ciphertext):
    margin = 0.25
    expected = get_freq(1)
    actual_mono_fitness = mono_fitness(ciphertext, expected)
    low_mono_fitness = abs(actual_mono_fitness - EXPECTED_MONO_FITNESS) > margin
    return similar_ioc(ciphertext) and low_mono_fitness


def letter_to_num(letters):
    return np.array([ALPHABET.index(letter) for letter in letters])


def num_to_letter(numbers):
    numbers = np.array(numbers)
    numbers %= len(ALPHABET)
    return "".join([ALPHABET[number] for number in numbers])


def invert_key(key):
    indexes = [key.index(letter) for letter in ALPHABET]
    return num_to_letter(indexes)


def encipher_mono_sub(plaintext, key):
    if isinstance(key, list):
        key = "".join(key)
    table = str.maketrans(ALPHABET, key)
    words = [word.translate(table) for word in plaintext.split()]
    return " ".join(words)


def decipher_mono_sub(ciphertext, key):
    return encipher_mono_sub(ciphertext, invert_key(key))


def atbash(text):
    key = ALPHABET[::-1]
    return encipher_mono_sub(text, key)


def swap_random(seq):
    seq = seq.copy()
    i, j = sample(range(len(seq)), 2)
    seq[i], seq[j] = seq[j], seq[i]
    return seq


def output_mono_sub(ciphertext, key):
    plaintext = decipher_mono_sub(ciphertext, key)
    print("Key:", key)
    print("Plaintext:", plaintext)


def hill_climbing_mono_sub_algorithm(ciphertext, init_key=None, fit_f=tetra_fitness):
    if init_key is None:
        init_key = ALPHABET
    parent_key = list(init_key)
    if fit_f == tetra_fitness:
        expected = get_freq(4)
    else:
        expected = get_freq(1)
    plaintext_attempt = decipher_mono_sub(ciphertext, parent_key)
    best_fitness = fit_f(plaintext_attempt, expected)
    counter = 0
    while counter < 10000:
        child_key = swap_random(parent_key)
        plaintext_attempt = decipher_mono_sub(ciphertext, child_key)
        fitness_attempt = fit_f(plaintext_attempt, expected)
        if fitness_attempt > best_fitness:
            parent_key = child_key.copy()
            best_fitness = fitness_attempt
            counter = 0
        counter += 1
    return best_fitness, "".join(parent_key)


def hill_climbing_mono_sub(ciphertext, init_key=None, fit_f=tetra_fitness):
    counter = 1
    limit = 20
    record = {}
    found = False
    while not found and counter <= limit:
        best_fitness, key = hill_climbing_mono_sub_algorithm(
            ciphertext, init_key, fit_f
        )
        record[key] = best_fitness
        print(counter, best_fitness, key)
        if best_fitness > CUTOFF_TETRA_FITNESS:
            found = True
        if counter == limit:
            key = max(record, key=record.get)
        counter += 1
    output_mono_sub(ciphertext, key)
    return key
