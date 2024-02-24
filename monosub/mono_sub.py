from random import sample

from ciphers.analysis import ALPHABET, fitness, get_freq, ioc, mono_fitness


def mono_sub_likely(ciphertext):
    expected = get_freq(1)
    similar_ioc = abs(ioc(ciphertext) - 1.73) < 0.2
    low_mono_fitness = abs(mono_fitness(ciphertext, expected) - 0.96) > 0.2
    return similar_ioc and low_mono_fitness


def invert_key(key):
    indexes = [key.index(letter) for letter in ALPHABET]
    return "".join([ALPHABET[index] for index in indexes])


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


def swap_random(seq):
    seq = seq.copy()
    i, j = sample(range(len(seq)), 2)
    seq[i], seq[j] = seq[j], seq[i]
    return seq


def output_mono_sub(ciphertext, key):
    plaintext = decipher_mono_sub(ciphertext, key)
    print("Key:", key)
    print("Plaintext:", plaintext)


def hill_climbing_mono_sub_algorithm(ciphertext, init_key=ALPHABET):
    parent_key = list(init_key)
    expected = get_freq(4)
    plaintext_attempt = decipher_mono_sub(ciphertext, parent_key)
    best_fitness = fitness(plaintext_attempt, expected)
    counter = 0
    while True:
        child_key = swap_random(parent_key)
        plaintext_attempt = decipher_mono_sub(ciphertext, child_key)
        fitness_attempt = fitness(plaintext_attempt, expected)
        if fitness_attempt > best_fitness:
            parent_key = child_key.copy()
            best_fitness = fitness_attempt
            counter = 0
        counter += 1
        if counter > 10000:
            break
    return best_fitness, "".join(parent_key)


def hill_climbing_mono_sub(ciphertext):
    counter = 0
    record = {}
    while True:
        best_fitness, key = hill_climbing_mono_sub_algorithm(ciphertext)
        record[key] = best_fitness
        counter += 1
        print(counter, best_fitness, key)
        if best_fitness > -10:
            break
        if counter > 50:
            key = max(record, key=record.get)
            break
    output_mono_sub(ciphertext, key)
    return key
