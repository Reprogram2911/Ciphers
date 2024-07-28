from itertools import product
from random import randrange

from ciphers.analysis import (
    ALPHABET,
    CUTOFF_TETRA_FITNESS,
    get_freq,
    get_words,
    split_into_slices,
    tetra_fitness,
)
from ciphers.monosub import letter_to_num, num_to_letter
from ciphers.polysub.vigenere import (
    brute_force_with_keywords,
    dictionary,
    get_period,
    hill_climbing,
)


def calculate_shift(num, version):
    shift = num // 2
    match version:
        case 1:
            pass
        case 2:
            shift = (13 - shift) % 13
    return shift


def porta(text, keyword, version):
    text = letter_to_num(text)
    keyword = letter_to_num(keyword)
    period = len(keyword)
    new_text = []
    for i, letter in enumerate(text):
        k = keyword[i % period]
        base = (letter + 13) % 26
        match version:
            case 1 | 2:
                shift = calculate_shift(k, version)
                if letter <= 12:
                    new_letter = base + shift
                    if new_letter > 25:
                        new_letter -= 13
                else:
                    a = [0] + list(range(12, 0, -1))
                    found_at = a.index(base)
                    new_index = (found_at + shift) % 13
                    new_letter = a[new_index]
            case 3:
                let = k % 13
                a = (
                    list(range(26 - let, 26))
                    + list(range(13, 26 - let))
                    + list(range(let, 13))
                    + list(range(0, let))
                )
                if k >= 13:
                    a.reverse()
                new_letter = a[letter]
        new_text.append(new_letter)
    return num_to_letter(new_text)


def encipher_porta(plaintext, keyword, version):
    return porta(plaintext, keyword, version)


def decipher_porta(ciphertext, keyword, version):
    return porta(ciphertext, keyword, version)


def encipher_bellaso(plaintext, keyword):
    return porta(plaintext, keyword, 3)


def decipher_bellaso(ciphertext, keyword):
    return porta(ciphertext, keyword, 3)


def output_porta(ciphertext, keyword, version):
    plaintext = decipher_porta(ciphertext, keyword, version)
    print("Keyword:", keyword)
    print("Version:", version)
    print("Plaintext:", plaintext)


def output_bellaso(ciphertext, keyword):
    plaintext = decipher_bellaso(ciphertext, keyword)
    print("Keyword:", keyword)
    print("Plaintext:", plaintext)


def brute_force_porta(ciphertext, period=None):
    if period is None:
        period = get_period(ciphertext)
    expected = get_freq(4)
    found = False
    poss_keywords = ["".join(i) for i in product(ALPHABET[::2], repeat=period)]
    for keyword in poss_keywords:
        print(keyword)
        for version in [1, 2]:
            poss_text = decipher_porta(ciphertext, keyword, version)
            fitness = tetra_fitness(poss_text, expected)
            if fitness > CUTOFF_TETRA_FITNESS:
                found = True
                break
    if found:
        output_porta(ciphertext, keyword, version)
    else:
        print("Brute-force attack failed")


def get_alt(letter):
    num = letter_to_num(letter)
    if num % 2 == 0:
        num += 1
    else:
        num -= 1
    return num_to_letter(num)


def matching_word(keyword):
    letters1 = keyword
    letters2 = [get_alt(i) for i in keyword]
    letters = [letters1, letters2]
    words = get_words()
    poss_indexes = list(product([0, 1], repeat=len(keyword)))
    for indexes in poss_indexes:
        word = []
        for index, which_group in enumerate(indexes):
            letter = letters[which_group][index]
            word.append(letter)
        word = "".join(word)
        if word in words:
            return word
    print("No matching word found")


def dictionary_porta(ciphertext):
    words = get_words()
    period = get_period(ciphertext)
    expected = get_freq(4)
    found = False
    highest = -500
    best = ""
    for word in words:
        if len(word) != period:
            continue
        print(word)
        for version in [1, 2]:
            poss_text = decipher_porta(ciphertext, word, version)
            fitness = tetra_fitness(poss_text, expected)
            if fitness > highest:
                highest = fitness
                best = (word, version)
            if fitness > CUTOFF_TETRA_FITNESS:
                found = True
                break
    if found:
        output_porta(ciphertext, word, version)
    else:
        print("Dictionary attack failed")
        print("Best:")
        output_porta(ciphertext, *best)


def hill_climbing_porta_algorithm(ciphertext, period, key=None):
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
            for v in [1, 2]:
                plaintext_attempt = decipher_porta(ciphertext, t_key, v)
                new_fitness = tetra_fitness(plaintext_attempt, expected)
                if new_fitness > current_fitness:
                    key = t_key.copy()
                    current_fitness = new_fitness
                    counter = 0
                    best_v = v
        if current_fitness > CUTOFF_TETRA_FITNESS:
            found = True
        counter += 1
    return current_fitness, "".join(key), best_v


def hill_climbing_porta(ciphertext, period=None, init_key=None, limit=20):
    if period is None:
        period = get_period(ciphertext)
    counter = 1
    record = {}
    found = False
    while not found and counter <= limit:
        best_fitness, key, best_v = hill_climbing_porta_algorithm(
            ciphertext, period, init_key
        )
        record[key] = best_fitness
        print(counter, best_fitness, key)
        if best_fitness > CUTOFF_TETRA_FITNESS:
            found = True
        if counter == limit:
            key = max(record, key=record.get)
        counter += 1
    output_porta(ciphertext, key, best_v)
    return key


def periodic_attack_porta_algo(ciphertext, period=None):
    if period is None:
        period = get_period(ciphertext)
    slices = split_into_slices(ciphertext, period)
    key = []
    for s in slices:
        k = hill_climbing_porta(s, period=1)
        key.append(k)
    return key


def periodic_attack_porta(ciphertext, period=None):
    key = periodic_attack_porta_algo(ciphertext, period)
    output_porta(ciphertext, key, 1)
    output_porta(ciphertext, key, 2)


def brute_force_bellaso(ciphertext, period=None):
    brute_force_with_keywords(ciphertext, decipher_bellaso, output_bellaso, period)


def dictionary_bellaso(ciphertext, period=None):
    dictionary(ciphertext, decipher_bellaso, output_bellaso, period)


def hill_climbing_bellaso(ciphertext, period=None):
    hill_climbing(ciphertext, decipher_bellaso, output_bellaso, period)
