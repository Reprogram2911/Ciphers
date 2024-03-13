from itertools import product
from random import randrange
import string

from ciphers.analysis import (
    ALPHABET,
    CUTOFF_TETRA_FITNESS,
    get_freq,
    tetra_fitness,
)
from ciphers.monosub import letter_to_num, num_to_letter
from ciphers.polysub.vigenere import get_period, periodic_attack

DIGITS = string.digits


def gronsfeld(text, key, encipher):
    text = letter_to_num(text)
    if isinstance(key, int):
        key = str(key)
    key = [int(letter) for letter in key]
    period = len(key)
    new_text = []
    for i, letter in enumerate(text):
        k = key[i % period]
        if encipher:
            new_letter = (letter + k) % len(ALPHABET)
        else:
            new_letter = (letter - k) % len(ALPHABET)
        new_text.append(new_letter)
    return num_to_letter(new_text)


def encipher_gronsfeld(plaintext, key):
    return gronsfeld(plaintext, key, True)


def decipher_gronsfeld(ciphertext, key):
    return gronsfeld(ciphertext, key, False)


def output_gronsfeld(ciphertext, key):
    plaintext = decipher_gronsfeld(ciphertext, key)
    print("Key:", key)
    print("Plaintext:", plaintext)


def brute_force_gronsfeld(ciphertext, period=None):
    if period is None:
        period = get_period(ciphertext)
    expected = get_freq(4)
    poss_keys = []
    found = False
    poss_keys += ["".join(i) for i in product(DIGITS, repeat=period)]
    for key in poss_keys:
        poss_text = decipher_gronsfeld(ciphertext, key)
        fitness = tetra_fitness(poss_text, expected)
        if fitness > CUTOFF_TETRA_FITNESS:
            found = True
            break
    if found:
        output_gronsfeld(ciphertext, key)
    else:
        print("Brute-force attack failed")


def hill_climbing_gronsfeld_algorithm(ciphertext, decipher, period, key=None):
    if key is None:
        key = [DIGITS[0]] * period
    else:
        key = list(key)
        assert period == len(key)
    expected = get_freq(4)
    current_fitness = tetra_fitness(ciphertext, expected)
    found = False
    counter = 0
    while not found and counter < 50:
        t_key = key.copy()
        rand_index = randrange(period)
        for digit in DIGITS:
            t_key[rand_index] = digit
            plaintext_attempt = decipher(ciphertext, t_key)
            new_fitness = tetra_fitness(plaintext_attempt, expected)
            if new_fitness > current_fitness:
                key = t_key.copy()
                current_fitness = new_fitness
                counter = 0
        if current_fitness > CUTOFF_TETRA_FITNESS:
            found = True
        counter += 1
    return current_fitness, "".join(key)


def hill_climbing_gronsfeld(ciphertext, decipher, output, period=None, init_key=None):
    if period is None:
        period = get_period(ciphertext)
    limit = 10
    counter = 1
    record = {}
    found = False
    while not found and counter <= limit:
        best_fitness, key = hill_climbing_gronsfeld_algorithm(
            ciphertext, decipher, period, init_key
        )
        record[key] = best_fitness
        print(counter, best_fitness, key)
        if best_fitness > CUTOFF_TETRA_FITNESS:
            found = True
        counter += 1
        if counter == limit:
            key = max(record, key=record.get)
    output(ciphertext, key)


def periodic_attack_gronsfeld(ciphertext, period=None):
    key = periodic_attack(ciphertext, period)
    key = "".join([str(i) for i in key])
    output_gronsfeld(ciphertext, key)
