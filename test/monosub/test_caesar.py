from ciphers.analysis import clean
from ciphers.monosub.caesar import (
    additive_inverse,
    brute_force_caesar,
    crib_caesar,
    decipher_caesar,
    encipher_caesar,
    mono_fitness_caesar,
)
from ciphers.test.utils import get_tests

if __name__ == "__main__":
    testing = "00000"
    testing = [int(i) for i in testing]

    tests = get_tests("testCaesar.txt")

    tests[2] = tests[2].split()
    tests = [
        test.replace("\n", "") if isinstance(test, str) else test for test in tests
    ]

    if testing[0]:
        print(528147 + 790378 % 62)
        print(72177 - 162737 % 81)
        for mod in 18, 19:
            for element in range(1, mod + 1):
                if additive_inverse(element, mod) == element:
                    print(mod, "/ 2 =", element)

    if testing[1]:
        test = clean(tests[0].upper())
        print(encipher_caesar(test, 11))
        print(decipher_caesar(tests[1], 15))

    if testing[2]:
        for test in tests[2]:
            brute_force_caesar(test)

    if testing[3]:
        crib_caesar(tests[3], "CUSTOM")
        cribs = "VICTORY SPAIN DISCO EUROVISION".split()
        for crib in cribs:
            print()
            crib_caesar(tests[4], crib)

    if testing[4]:
        longs = tests[5:]
        shorts = tests[2]
        for test in longs:
            mono_fitness_caesar(test, chi2=True)
            mono_fitness_caesar(test)
        for test in shorts:
            mono_fitness_caesar(test, chi2=True)  # fails
            mono_fitness_caesar(test)  # fails (but second one should pass?)
