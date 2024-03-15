from ciphers.polysub.gronsfeld import (
    brute_force_gronsfeld,
    decipher_gronsfeld,
    hill_climbing_gronsfeld,
    periodic_attack_gronsfeld,
)
from ciphers.test.utils import get_tests


if __name__ == "__main__":
    testing = "0000"
    testing = [int(i) for i in testing]

    tests = get_tests("testGronsfeld.txt")
    tests = [test.replace("\n", "") for test in tests]

    if testing[0]:
        print(decipher_gronsfeld(tests[0], 78345024))

    if testing[1]:
        brute_force_gronsfeld(tests[1])  # 759

    if testing[2]:
        hill_climbing_gronsfeld(tests[2])  # 2305639

    if testing[3]:
        periodic_attack_gronsfeld(tests[3])  # 85340
