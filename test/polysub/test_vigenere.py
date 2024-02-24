from ciphers.polysub.vigenere import (
    brute_force_vigenere,
    decipher_vigenere,
    encipher_vigenere,
)
from ciphers.test.analysis import get_tests

if __name__ == "__main__":
    testing = "01"
    testing = [int(i) for i in testing]

    tests = get_tests("testVigenere.txt")
    tests = [test.replace("\n", "") for test in tests]

    if testing[0]:
        tests[0] = tests[0].replace(" ", "")
        print(encipher_vigenere(tests[0], "PACMAN"))
        print(decipher_vigenere(tests[1], "VIGENERE"))

    if testing[1]:
        for test in tests[2:]:
            brute_force_vigenere(test)
            # DEDE, IBM
