import matplotlib.pyplot as plt

from ciphers.analysis import (
    ALPHABET,
    get_freq,
    mono_fitness,
    mono_fitness_chi2,
    split_into_ngrams,
    tetra_fitness,
)
from ciphers.monosub.mono_sub import (
    decipher_mono_sub,
    encipher_mono_sub,
    letter_to_num,
)


def additive_inverse(number, mod):
    return (-number) % mod


def generate_alphabet_caesar(number):
    return ALPHABET[number:] + ALPHABET[:number]


def generate_alphabet_caesar_2(number):
    output = []
    for index, letter in enumerate(ALPHABET):
        new_index = (index + number) % len(ALPHABET)
        output.append(ALPHABET[new_index])
    return output


def encipher_caesar(plaintext, key):
    key = generate_alphabet_caesar(key)
    return encipher_mono_sub(plaintext, key)


def decipher_caesar(ciphertext, key=None):
    key = generate_alphabet_caesar(key)
    return decipher_mono_sub(ciphertext, key)


def albam(text):
    return encipher_caesar(text, 13)


def output_caesar(ciphertext, key):
    plaintext = decipher_caesar(ciphertext, key)
    print("Key:", key)
    print("Plaintext:", plaintext)


def brute_force_caesar(ciphertext):
    expected = get_freq(4)
    poss_texts = {key: decipher_caesar(ciphertext, key) for key in range(len(ALPHABET))}
    fitnesses = {
        key: tetra_fitness(poss_text, expected) for key, poss_text in poss_texts.items()
    }
    key = max(fitnesses, key=fitnesses.get)
    output_caesar(ciphertext, key)
    return key


def all_equal(seq):
    return seq.count(seq[0]) == len(seq)


def crib_caesar(ciphertext, crib):
    n = len(crib)
    ngrams = split_into_ngrams(ciphertext, n)
    found = False
    for ngram in ngrams:
        shifts = []
        for letters in zip(ngram, crib):
            i, j = letter_to_num(letters)
            shift = (i - j) % len(ALPHABET)
            shifts.append(shift)
        if all_equal(shifts):
            key = shifts[0]
            output_caesar(ciphertext, key)
            found = True
            break
    if not found:
        print("Key not found with crib", crib)


def mono_fitness_caesar(ciphertext, chi2=False, graph=True, output=False):
    expected = get_freq(1)
    poss_texts = [decipher_caesar(ciphertext, k) for k in range(len(ALPHABET))]
    if chi2:
        fitnesses = [mono_fitness_chi2(poss_text, expected) for poss_text in poss_texts]
    else:
        fitnesses = [mono_fitness(poss_text, expected) for poss_text in poss_texts]
    if graph:
        xs = list(range(len(ALPHABET)))
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.spines["bottom"].set_position("zero")  # accomodates for negative chi2 values
        plt.bar(xs, fitnesses)
        plt.xticks(xs)
        plt.show()
        plt.close()
    key = fitnesses.index(max(fitnesses))
    if output:
        output_caesar(ciphertext, key)
    return key
