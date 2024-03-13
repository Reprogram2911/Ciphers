from ciphers.analysis import clean, find_block_size
from ciphers.polysub.vigenere import (
    brute_force_vigenere,
    crib_vigenere,
    decipher_vigenere,
    dictionary_vigenere,
    encipher_vigenere,
    hill_climbing_vigenere,
    periodic_attack_vigenere,
)
from ciphers.test.analysis import get_tests

if __name__ == "__main__":
    testing = "0000001"
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

    if testing[2]:
        test = tests[4]
        crib_vigenere(test, "NATIONALSECURITY")
        print(decipher_vigenere(test, "SCANDAL"))

    if testing[3]:
        dictionary_vigenere(tests[5])  # SECRET

    if testing[4]:
        test = tests[6]
        find_block_size(test)  # 5
        hill_climbing_vigenere(test, 5)
        # PROOF

    if testing[5]:
        test = tests[7]
        # find_block_size(test)  # 5? 10? 20? 40
        # hill_climbing_vigenere(test, 40)
        # found plaintext words:
        # ORNAMENTEDWITHHEARTS, SHAPEDLIKETHE, DIAMONDS, CAMETENSOLDIERS, CARRYING,
        # GARDEN, LITTLE, ROYALCHILDREN, WALKEDTWOANDTWO
        plaintext = clean(
            "First came ten soldiers carrying clubs; these were all shaped like the three gardeners, "
            "oblong and flat, with their hands and feet at the corners: next the ten courtiers; these were "
            "ornamented all over with diamonds, and walked two and two, as the soldiers did. After these "
            "came the royal children; there were ten of them, and the little dears came jumping merrily "
            "along hand in hand, in couples: they were all ornamented with hearts."
        ).replace(" ", "")
        print(decipher_vigenere(test, plaintext))
        key = "FTUNGPOMEACXIOVUOCBEQYXTVKLGPFFDXJSOZHEK"
        hill_climbing_vigenere(key, 5)
        keys = ["CLUBS", "DIAMONDS"]
        print(decipher_vigenere(decipher_vigenere(test, keys[0]), keys[1]))
        print(decipher_vigenere(decipher_vigenere(test, keys[1]), keys[0]))

    if testing[6]:
        periodic_attack_vigenere(tests[8])
        # STING
