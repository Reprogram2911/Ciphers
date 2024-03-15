from ciphers.polysub.variant_beaufort import (
    brute_force_variant_beaufort,
    convert_variant_beaufort_to_vigenere,
    decipher_variant_beaufort,
    dictionary_variant_beaufort,
    hill_climbing_variant_beaufort,
    periodic_attack_variant_beaufort,
)
from ciphers.test.utils import get_tests

if __name__ == "__main__":
    testing = "00000"
    testing = [int(i) for i in testing]

    tests = get_tests("testVariantBeaufort.txt")
    tests = [test.replace("\n", "") for test in tests]

    if testing[0]:
        keyword = "TOWER"
        print(decipher_variant_beaufort(tests[0], keyword))
        print(convert_variant_beaufort_to_vigenere(keyword))  # HMEWJ

    if testing[1]:
        brute_force_variant_beaufort(tests[1])  # AGE
        print(convert_variant_beaufort_to_vigenere("AGE"))  # AUW

    if testing[2]:
        dictionary_variant_beaufort(tests[2])  # TREASURE

    if testing[3]:
        hill_climbing_variant_beaufort(tests[3])  # ALICE

    if testing[4]:
        ciphertext = tests[4]
        periodic_attack_variant_beaufort(ciphertext)  # fails, LMSIMN
        hill_climbing_variant_beaufort(ciphertext)  # POISON
