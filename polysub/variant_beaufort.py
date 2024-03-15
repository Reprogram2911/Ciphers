from ciphers.monosub import atbash, encipher_caesar, num_to_letter
from ciphers.polysub.vigenere import (
    brute_force_with_keywords,
    decipher_vigenere,
    dictionary,
    encipher_vigenere,
    hill_climbing,
    periodic_attack,
)


def encipher_variant_beaufort(plaintext, keyword):
    return decipher_vigenere(plaintext, keyword)


def decipher_variant_beaufort(ciphertext, keyword):
    return encipher_vigenere(ciphertext, keyword)


def convert_variant_beaufort_to_vigenere(key):
    return encipher_caesar(atbash(key), 1)


def output_variant_beaufort(ciphertext, keyword):
    plaintext = decipher_variant_beaufort(ciphertext, keyword)
    print("Keyword:", keyword)
    print("Plaintext:", plaintext)


def brute_force_variant_beaufort(ciphertext, period=None):
    return brute_force_with_keywords(
        ciphertext, decipher_variant_beaufort, output_variant_beaufort, period
    )


def dictionary_variant_beaufort(ciphertext):
    dictionary(ciphertext, decipher_variant_beaufort, output_variant_beaufort)


def hill_climbing_variant_beaufort(ciphertext, period=None, init_key=None):
    hill_climbing(
        ciphertext, decipher_variant_beaufort, output_variant_beaufort, period, init_key
    )


def periodic_attack_variant_beaufort(ciphertext, period=None):
    key = periodic_attack(ciphertext, period)
    key = num_to_letter(key)
    output_variant_beaufort(ciphertext, key)
