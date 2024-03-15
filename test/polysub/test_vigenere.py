from ciphers.analysis import find_period_auto
from ciphers.polysub.vigenere import (
    brute_force_vigenere,
    crib_vigenere,
    decipher_vigenere,
    dictionary_vigenere,
    encipher_vigenere,
    hill_climbing_vigenere,
    periodic_attack_vigenere,
)
from ciphers.test.utils import get_tests

if __name__ == "__main__":
    testing = "0000000"
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
            # DE, IBM

    if testing[2]:
        test = tests[4]
        crib_vigenere(test, "NATIONALSECURITY")  # DALSCANDALSCANDA
        print(decipher_vigenere(test, "SCANDAL"))

    if testing[3]:
        dictionary_vigenere(tests[5])  # SECRET

    if testing[4]:
        test = tests[6]
        period = find_period_auto(test)
        hill_climbing_vigenere(test, period)  # PROOF

    if testing[5]:
        test = tests[7]
        period = find_period_auto(test)  # 40
        combined_key = hill_climbing_vigenere(test, period)
        # FTUNGPOMEACXIOVUOCBEQYXTVKLGPFFDAMJOZHEK
        hill_climbing_vigenere(combined_key)  # period = 5
        keys = ["CLUBS", "DIAMONDS"]
        plaintext_1 = decipher_vigenere(decipher_vigenere(test, keys[0]), keys[1])
        plaintext_2 = decipher_vigenere(decipher_vigenere(test, keys[1]), keys[0])
        assert plaintext_1 == plaintext_2

    if testing[6]:
        periodic_attack_vigenere(tests[8])  # STING
