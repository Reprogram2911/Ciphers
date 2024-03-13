from ciphers.analysis import ALPHABET
from ciphers.monosub import num_to_letter
from ciphers.polysub.poly_sub import decipher_poly_sub, encipher_poly_sub
from ciphers.polysub.vigenere import (
    brute_force_with_keywords,
    dictionary,
    hill_climbing,
    periodic_attack,
)

REVERSED_ALPHABET = ALPHABET[::-1]


def generate_alphabet_beaufort(letter):
    number = REVERSED_ALPHABET.index(letter)
    return REVERSED_ALPHABET[number:] + REVERSED_ALPHABET[:number]


def encipher_beaufort(plaintext, keyword):
    keys = [generate_alphabet_beaufort(letter) for letter in keyword]
    return encipher_poly_sub(plaintext, keys)


def decipher_beaufort(plaintext, keyword):
    keys = [generate_alphabet_beaufort(letter) for letter in keyword]
    return decipher_poly_sub(plaintext, keys)


def output_beaufort(ciphertext, keyword):
    plaintext = decipher_beaufort(ciphertext, keyword)
    print("Keyword:", keyword)
    print("Plaintext:", plaintext)


def brute_force_beaufort(ciphertext, period=None):
    brute_force_with_keywords(ciphertext, decipher_beaufort, output_beaufort, period)


def dictionary_beaufort(ciphertext):
    dictionary(ciphertext, decipher_beaufort, output_beaufort)


def hill_climbing_beaufort(ciphertext, period=None, init_key=None):
    hill_climbing(ciphertext, decipher_beaufort, output_beaufort, period, init_key)


def periodic_attack_beaufort(ciphertext, period=None):
    key = periodic_attack(ciphertext, period)
    key = num_to_letter(key)
    output_beaufort(ciphertext, key)
