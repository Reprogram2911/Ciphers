from ciphers.analysis import analyse_frequencies, strip
from ciphers.monosub import hill_climbing_mono_sub, invert_key
from ciphers.monosub.keyword import (
    decipher_keyword,
    dictionary_keyword,
    encipher_keyword,
    generate_alphabet_keyword,
)
from ciphers.test.analysis import get_tests

if __name__ == "__main__":
    testing = "0000"
    testing = [int(i) for i in testing]

    tests = get_tests("testKeyword.txt")
    tests[0] = strip(tests[0])
    tests[1:] = [test.replace("\n", "") for test in tests[1:]]
    tests[2] = tests[2].replace(" ", "")
    tests[4] = tests[4].replace(" ", "")

    if testing[0]:
        word = "AUTOMOBILE"
        for i in range(1, 4):
            print(generate_alphabet_keyword(word, i))

    if testing[1]:
        print(encipher_keyword(tests[0], "KNIGHTS", 1))
        print(decipher_keyword(tests[1], "ROUNDTABLE", 2))

    if testing[2]:
        test = tests[2]
        analyse_frequencies(test)  # L is most common
        test = test.replace("L", "")
        key = hill_climbing_mono_sub(test)  # DFIGXHJKCSNPQROMUEBTALVWYZ
        print(invert_key(key))  # USIARBDFCGHJPKOLMNVTQWXEYZ

    if testing[3]:
        dictionary_keyword(tests[3])  # BRAVE, method=2
        dictionary_keyword(tests[4])  # EDGAR, method=2
