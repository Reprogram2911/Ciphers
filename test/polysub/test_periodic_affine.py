from ciphers.analysis import clean
from ciphers.monosub import num_to_letter
from ciphers.polysub.periodic_affine import (
    decipher_periodic_affine,
    encipher_periodic_affine,
    periodic_attack_periodic_affine,
)
from ciphers.test.utils import get_tests


def convert_keys(s):
    keys = s.split(";")
    keys = [k.replace(" ", "").split(",") for k in keys]
    return [[int(i) for i in sublist] for sublist in keys]


if __name__ == "__main__":
    testing = "001"
    testing = [int(i) for i in testing]

    tests = get_tests("testPeriodicAffine.txt")
    tests = [clean(test).replace(" ", "") for test in tests]

    if testing[0]:
        keys = convert_keys("5, 8; 11, 2; 21, 18")
        print(encipher_periodic_affine(tests[0], keys))
        keys = convert_keys("3, 4; 5, 6; 7, 8; 9, 10; 11, 12; 25, 24")
        print(encipher_periodic_affine(tests[1], keys))

    if testing[1]:
        keys = convert_keys("11, 9; 9, 8; 7, 6; 5, 4; 3, 2")
        print(decipher_periodic_affine(tests[2], keys))

    if testing[2]:
        periodic_attack_periodic_affine(tests[3], period=6)
        # Keys: [1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]
        periodic_attack_periodic_affine(tests[4], period=15)
        keys = [
            [7, 0],
            [7, 6],
            [7, 17],
            [7, 8],
            [7, 2],
            [7, 14],
            [7, 11],
            [7, 0],
            [7, 4],
            [7, 12],
            [7, 14],
            [7, 17],
            [7, 19],
            [7, 4],
            [7, 12],
        ]
        keys = [k for sublist in keys for k in sublist]
        print(num_to_letter(keys[1::2]))
        # AGRICOLAEMORTEM
