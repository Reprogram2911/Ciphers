from ciphers.analysis import analyse_frequencies, strip
from ciphers.monosub import brute_force_caesar, brute_force_affine
from ciphers.monosub.keyword import (
    decipher_keyword,
    encipher_keyword,
    generate_alphabet_keyword,
)
from ciphers.test.analysis import get_tests

if __name__ == "__main__":
    testing = "001"
    testing = [int(i) for i in testing]

    tests = get_tests("testKeyword.txt")
    tests[0] = strip(tests[0])
    tests[1:] = [test.replace("\n", "") for test in tests[1:]]
    tests[2] = tests[2].replace(" ", "")

    if testing[0]:
        word = "AUTOMOBILE"
        for i in range(1, 4):
            print(generate_alphabet_keyword(word, i))

    if testing[1]:
        print(encipher_keyword(tests[0], "KNIGHTS", 1))
        print(decipher_keyword(tests[1], "ROUNDTABLE", 2))

    if testing[2]:
        # analyse_frequencies(tests[2])  # L is most common
        spaceless = tests[2].replace("L", "")
        # brute_force_caesar(spaceless)
        # brute_force_affine(spaceless)
