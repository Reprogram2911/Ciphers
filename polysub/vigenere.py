from collections import Counter
from itertools import product
from random import randrange

from ciphers.analysis import (
    ALPHABET,
    CUTOFF_TETRA_FITNESS,
    get_freq,
    get_words,
    plot_period_graph,
    split_into_ngrams,
    tetra_fitness,
)
from ciphers.monosub import (
    letter_to_num,
    mono_fitness_caesar,
    num_to_letter,
    remove_duplicates,
)
from ciphers.polysub.poly_sub import split_into_slices


def vigenere(text, keyword, encipher):
    text = letter_to_num(text)
    keyword = letter_to_num(keyword)
    period = len(keyword)
    new_text = []
    for i, letter in enumerate(text):
        k = keyword[i % period]
        if encipher:
            new_letter = (letter + k) % len(ALPHABET)
        else:
            new_letter = (letter - k) % len(ALPHABET)
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


def get_period(ciphertext):
    plot_period_graph(ciphertext)
    return int(input("Period: "))


def brute_force_with_keywords(ciphertext, decipher, output, period=None):
    if period is None:
        period = get_period(ciphertext)
    expected = get_freq(4)
    found = False
    poss_keywords = ["".join(i) for i in product(ALPHABET, repeat=period)]
    for keyword in poss_keywords:
        print(keyword)
        poss_text = decipher(ciphertext, keyword)
        fitness = tetra_fitness(poss_text, expected)
        if fitness > CUTOFF_TETRA_FITNESS:
            found = True
            break
    if found:
        output(ciphertext, keyword)
    else:
        print("Brute-force attack failed")


def brute_force_vigenere(ciphertext):
    brute_force_with_keywords(ciphertext, decipher_vigenere, output_vigenere)


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


def dictionary(ciphertext, decipher, output, period=None):
    if period is None:
        period = get_period(ciphertext)
    words = get_words()
    expected = get_freq(4)
    highest_f = -500
    best_word = ""
    found = False
    for word in words:
        if len(word) != period:
            continue
        print(word)
        poss_text = decipher(ciphertext, word)
        fitness = tetra_fitness(poss_text, expected)
        if fitness > CUTOFF_TETRA_FITNESS:
            found = True
            break
        if fitness > highest_f:
            highest_f = fitness
            best_word = word
    if found:
        output(ciphertext, word)
    else:
        print("Dictionary attack failed; best found was")
        output(ciphertext, best_word)


def dictionary_vigenere(ciphertext):
    dictionary(ciphertext, decipher_vigenere, output_vigenere)


def hill_climbing_algorithm(ciphertext, decipher, period, key=None):
    if key is None:
        key = [ALPHABET[0]] * period
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
        for letter in ALPHABET:
            t_key[rand_index] = letter
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


def hill_climbing(ciphertext, decipher, output, period=None, init_key=None, limit=20):
    if period is None:
        period = get_period(ciphertext)
    counter = 1
    record = {}
    found = False
    while not found and counter <= limit:
        best_fitness, key = hill_climbing_algorithm(
            ciphertext, decipher, period, init_key
        )
        record[key] = best_fitness
        print(counter, best_fitness, key)
        if best_fitness > CUTOFF_TETRA_FITNESS:
            found = True
        if counter == limit:
            key = max(record, key=record.get)
        counter += 1
    output(ciphertext, key)


def hill_climbing_vigenere(ciphertext, period=None, init_key=None):
    hill_climbing(ciphertext, decipher_vigenere, output_vigenere, period, init_key)


def periodic_attack(ciphertext, period=None):
    if period is None:
        period = get_period(ciphertext)
    slices = split_into_slices(ciphertext, period)
    key = []
    for s in slices:
        k = mono_fitness_caesar(s, output=False)
        key.append(k)
    return key


def periodic_attack_vigenere(ciphertext, period=None):
    key = periodic_attack(ciphertext, period)
    key = num_to_letter(key)
    output_vigenere(ciphertext, key)
