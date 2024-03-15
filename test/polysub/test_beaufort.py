from ciphers.monosub import atbash, encipher_caesar
from ciphers.polysub import encipher_vigenere
from ciphers.polysub.beaufort import (
    brute_force_beaufort,
    decipher_beaufort,
    dictionary_beaufort,
    encipher_beaufort,
    hill_climbing_beaufort,
    periodic_attack_beaufort,
)
from ciphers.test.utils import get_tests

if __name__ == "__main__":
    testing = "000000"
    testing = [int(i) for i in testing]

    tests = get_tests("testBeaufort.txt")
    tests = [test.replace("\n", "") for test in tests]

    if testing[0]:
        print(decipher_beaufort(tests[0], "HUSBAND"))

    if testing[1]:
        brute_force_beaufort(tests[1])  # SEA

    if testing[2]:
        dictionary_beaufort(tests[2])  # WOMEN

    if testing[3]:
        hill_climbing_beaufort(tests[3])  # NOMAD

    if testing[4]:
        ciphertext = tests[4]
        periodic_attack_beaufort(ciphertext)  # fails, HAIRTXQC
        hill_climbing_beaufort(ciphertext)  # SHERLOCK

    if testing[5]:
        beaufort_key = "BEAUFORT"
        vigenere_key = atbash(beaufort_key)
        atbash_key = encipher_caesar(beaufort_key, 1)
        plaintext = "PETERPIPERPICKEDAPECKOFPICKLEDPEPPERS"
        ciphertext_1 = encipher_beaufort(plaintext, beaufort_key)
        ciphertext_2 = atbash(encipher_vigenere(plaintext, vigenere_key))
        ciphertext_3 = encipher_vigenere(atbash(plaintext), atbash_key)
        assert ciphertext_1 == ciphertext_2 == ciphertext_3
