from ciphers.analysis import clean, find_period_auto
from ciphers.polysub.poly_sub import (
    decipher_poly_sub,
    encipher_poly_sub,
    find_period_repeats,
    find_period_twist,
    hill_climbing_poly_sub,
)
from ciphers.test.utils import get_tests

if __name__ == "__main__":
    testing = "00001"
    testing = [int(i) for i in testing]

    tests = get_tests("testPolySub.txt")

    if testing[0]:
        keys = tests[0].split("\n")
        plaintext = clean(tests[1]).replace(" ", "")
        ciphertext = tests[2].replace("\n", "")
        print(encipher_poly_sub(plaintext, keys))
        print(decipher_poly_sub(ciphertext, keys))

    if testing[1]:
        for test in tests[2:]:
            test = test.replace("\n", "")
            try:
                print(find_period_repeats(test))  # x, 7, 5, 5
            except ValueError as e:
                print(e)

    if testing[2]:
        for test in tests[2:]:
            test = test.replace("\n", "")
            find_period_auto(test)  # 3, 7, 5, 5

    if testing[3]:
        for test in tests[2:]:
            test = test.replace("\n", "")
            find_period_twist(test)  # unreliable

    if testing[4]:
        test = tests[6].replace("\n", "")
        hill_climbing_poly_sub(test, period=4)
        # TODO: rewrite in C++
