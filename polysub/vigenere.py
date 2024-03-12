from collections import Counter
from itertools import product
from random import randrange

from ciphers.analysis import (
    ALPHABET,
    CUTOFF_TETRA_FITNESS,
    WORDS_FP,
    get_freq,
    read_dict,
    split_into_ngrams,
    tetra_fitness,
)
from ciphers.monosub import letter_to_num, num_to_letter, remove_duplicates


def vigenere(text, keyword, encipher):
    text = letter_to_num(text)
    keyword = letter_to_num(keyword)
    period = len(keyword)
    new_text = []
    for i, letter in enumerate(text):
        k = keyword[i % period]
        if encipher:
            new_letter = (letter + k) % 26
        else:
            new_letter = (letter - k) % 26
        new_text.append(new_letter)
    return num_to_letter(new_text)


def encipher_vigenere(plaintext, keyword):
    return vigenere(plaintext, keyword, True)


def decipher_vigenere(ciphertext, keyword):
    return vigenere(ciphertext, keyword, False)


def output_vigenere(ciphertext, keyword):
    plaintext = decipher_vigenere(ciphertext, keyword)
    print("Keyword:", keyword)
    print("Plaintext:", plaintext)


def brute_force_vigenere(ciphertext):
    expected = get_freq(4)
    poss_keywords = []
    for i in range(3, 5):
        poss_keywords += ["".join(i) for i in product(ALPHABET, repeat=i)]
    for keyword in poss_keywords:
        poss_text = decipher_vigenere(ciphertext, keyword)
        fitness = tetra_fitness(poss_text, expected)
        if fitness > CUTOFF_TETRA_FITNESS:
            break
    output_vigenere(ciphertext, keyword)


def crib_vigenere(ciphertext, crib):
    n = len(crib)
    ngrams = split_into_ngrams(ciphertext, n)
    crib = letter_to_num(crib)
    poss_keys = []
    for ngram in ngrams:
        poss_key = [(x - y) % len(ALPHABET) for x, y in zip(letter_to_num(ngram), crib)]
        for i in range(5, n // 2 + 1):
            inner_ngrams = split_into_ngrams(poss_key, i)
            inner_ngrams = [num_to_letter(inner_ngram) for inner_ngram in inner_ngrams]
            inner_ngrams = Counter(inner_ngrams)
            inner_ngrams = {
                inner_ngram: count
                for inner_ngram, count in inner_ngrams.items()
                if count > 1
            }
            if inner_ngrams != {}:
                poss_keys.append(num_to_letter(poss_key))
    print("Possible keys:")
    print("\n".join(remove_duplicates(poss_keys)))


def dictionary_vigenere(ciphertext):
    words = read_dict(WORDS_FP).keys()

    expected = get_freq(4)

    for word in words:
        poss_text = decipher_vigenere(ciphertext, word)
        fitness = tetra_fitness(poss_text, expected)

        if fitness > CUTOFF_TETRA_FITNESS:
            break

    output_vigenere(ciphertext, word)


def hill_climbing_vigenere_algorithm(ciphertext, period, key=None):
    if key is None:
        key = ["A"] * period
    else:
        key = list(key)
        assert period == len(key)
    expected = get_freq(4)
    current_fitness = tetra_fitness(ciphertext, expected)
    found = False
    counter = 0

    while not found and counter < 100:
        t_key = key.copy()
        rand_index = randrange(period)
        for letter in ALPHABET:
            t_key[rand_index] = letter
            plaintext_attempt = decipher_vigenere(ciphertext, t_key)
            new_fitness = tetra_fitness(plaintext_attempt, expected)
            if new_fitness > current_fitness:
                key = t_key.copy()
                current_fitness = new_fitness

        if current_fitness > CUTOFF_TETRA_FITNESS:
            found = True

        counter += 1

    return current_fitness, "".join(key)


def hill_climbing_vigenere(ciphertext, period=None, init_key=None):
    limit = 50
    counter = 1
    record = {}
    found = False
    while not found and counter <= limit:
        if period is None:
            for i in range(5, 11):
                best_fitness, key = hill_climbing_vigenere_algorithm(
                    ciphertext, i, init_key
                )
                record[key] = best_fitness
                print(counter, i, best_fitness, key)
                if best_fitness > CUTOFF_TETRA_FITNESS:
                    found = True
                    break
        else:
            best_fitness, key = hill_climbing_vigenere_algorithm(
                ciphertext, period, init_key
            )
            record[key] = best_fitness
            print(counter, best_fitness, key)
            if best_fitness > CUTOFF_TETRA_FITNESS:
                found = True
        if counter == limit:
            key = max(record, key=record.get)
        counter += 1
    output_vigenere(ciphertext, key)
    return key
