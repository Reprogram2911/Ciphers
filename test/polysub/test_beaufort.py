from ciphers.polysub.beaufort import (
    brute_force_beaufort,
    decipher_beaufort,
    dictionary_beaufort,
    hill_climbing_beaufort,
    periodic_attack_beaufort,
)
from ciphers.test.analysis import get_tests

if __name__ == "__main__":
    testing = "00000"
    testing = [int(i) for i in testing]

    tests = get_tests("testBeaufort.txt")
    tests = [test.replace("\n", "") for test in tests]

    if testing[0]:
        print(decipher_beaufort(tests[0], "HUSBAND"))

    if testing[1]:
        brute_force_beaufort(tests[1], 3)
        # SEA

    if testing[2]:
        dictionary_beaufort(tests[2])
        # WOMEN

    if testing[3]:
        hill_climbing_beaufort(tests[3])
        # NOMAD

    if testing[4]:
        ciphertext = tests[4]
        periodic_attack_beaufort(ciphertext)  # fails, HAIRTXQC
        hill_climbing_beaufort(ciphertext)
        # SHERLOCK
