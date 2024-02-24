from itertools import product

from ciphers.analysis import ALPHABET, get_freq, tetra_fitness
from ciphers.monosub import letter_to_num, num_to_letter


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
        if fitness > -10:
            break
    output_vigenere(ciphertext, keyword)
