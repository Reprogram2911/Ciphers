from random import randint

from ciphers.analysis import strip, ALPHABET
from ciphers.monosub.affine import (
    gcd,
    lcm,
    lcm2,
    multiplicative_inverse,
    valid_key_affine,
    encipher_affine,
    decipher_affine,
    brute_force_affine,
)


def two_random_numbers(lowest=1, highest=50):
    num1 = randint(lowest, highest)
    num2 = randint(lowest, highest)
    while num2 <= num1:
        num2 = randint(lowest, highest)
    return num1, num2


def random_a_b():
    a, b = two_random_numbers(0, 25)
    while not valid_key_affine(a):
        a = randint(0, 25)
    return a, b


def generate_extended_alphabet(a, b):
    if not valid_key_affine(a):
        raise ValueError("Multiplier is not invertible")
    output = []
    extended_alphabet = ALPHABET + " "
    for index, letter in enumerate(extended_alphabet):
        new_index = (a * index + b) % 27
        output.append(extended_alphabet[new_index])
    return output


if __name__ == "__main__":
    testing = "0000000"
    testing = [int(i) for i in testing]

    with open("testAffine.txt", "r") as f:
        tests = f.read().split("\n\n")
    tests = [strip(test).replace("\n", "") for test in tests]
    tests = [test.replace(" ", "") if i != 0 else test for i, test in enumerate(tests)]

    if testing[0]:
        for _ in range(5):
            num1, num2 = two_random_numbers()
            print(num1, num2)
            print("GCD:", gcd(num1, num2))
            print("LCM1:", lcm(num1, num2))
            print("LCM2:", lcm2(num1, num2))
            print("GCD * LCM2:", gcd(num1, num2) * lcm2(num1, num2))
            print("NUM1 * NUM2:", num1 * num2)
            print()

    if testing[1]:
        for _ in range(5):
            num1, num2 = two_random_numbers()
            print(num1, num2)
            print(multiplicative_inverse(num1, num2))
            print()

    if testing[2]:
        keyspace = 0
        for a in range(26):
            for b in range(26):
                if valid_key_affine(a):
                    keyspace += 1
        print(keyspace)  # 312

    if testing[3]:
        print(encipher_affine(tests[0], 11, 9))
        print(decipher_affine(tests[1], 15, 3))

    if testing[4]:
        keyspace = 0
        for a in range(27):
            for b in range(27):
                if valid_key_affine(a):
                    keyspace += 1
        print(keyspace)  # 324

    if testing[5]:
        m, n = random_a_b()
        print(m, n)

        p, q = random_a_b()
        print(p, q)

        # p * (m * i + n) + q = pm * i + (pn + q)
        r = p * m
        s = p * n + q
        print(valid_key_affine(r))
        print(encipher_affine(encipher_affine(tests[0], m, n), p, q))
        if valid_key_affine(r):
            print(encipher_affine(tests[0], r, s))

    if testing[6]:
        brute_force_affine(tests[2])
