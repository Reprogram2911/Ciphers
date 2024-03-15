from random import randint

from ciphers.analysis import ALPHABET, clean, split_into_blocks
from ciphers.monosub import letter_to_num
from ciphers.monosub.affine import (
    brute_force_affine,
    crib_affine,
    decipher_affine,
    encipher_affine,
    gcd,
    lcm,
    lcm_2,
    mono_fitness_affine,
    multiplicative_inverse,
    solve_for_a,
    solve_for_b,
    valid_key_affine,
)
from ciphers.test.utils import get_tests


def two_random_numbers(lowest=1, highest=50):
    num1 = randint(lowest, highest)
    num2 = randint(lowest, highest)
    while num2 <= num1:
        num2 = randint(lowest, highest)
    return num1, num2


def random_a_b():
    highest = len(ALPHABET) - 1
    a, b = two_random_numbers(0, highest)
    while not valid_key_affine(a):
        a = randint(0, highest)
    return a, b


def generate_extended_alphabet(a, b):
    if not valid_key_affine(a):
        raise ValueError("Multiplier is not invertible")
    output = []
    extended_alphabet = ALPHABET + " "
    for index, letter in enumerate(extended_alphabet):
        new_index = (a * index + b) % len(extended_alphabet)
        output.append(extended_alphabet[new_index])
    return output


def flatten_list(ls):
    return [e for i in ls for e in i]


if __name__ == "__main__":
    testing = "0000000000"
    testing = [int(i) for i in testing]

    tests = get_tests("testAffine.txt")
    tests = [clean(test) for test in tests]
    tests = [test.replace(" ", "") if i != 0 else test for i, test in enumerate(tests)]

    if testing[0]:
        for _ in range(5):
            num1, num2 = two_random_numbers()
            print(num1, num2)
            print("GCD:", gcd(num1, num2))
            print("LCM1:", lcm(num1, num2))
            print("LCM2:", lcm_2(num1, num2))
            print("GCD * LCM2:", gcd(num1, num2) * lcm_2(num1, num2))
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
        poss = len(ALPHABET)
        for a in range(poss):
            for b in range(poss):
                if valid_key_affine(a):
                    keyspace += 1
        print(keyspace)  # 312

    if testing[3]:
        print(encipher_affine(tests[0], 11, 9))
        print(decipher_affine(tests[1], 15, 3))

    if testing[4]:
        keyspace = 0
        poss = len(ALPHABET) + 1
        for a in range(poss):
            for b in range(poss):
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
        brute_force_affine(tests[2])  # 23, 8

    if testing[7]:
        crib = letter_to_num("CRIB")
        ngram = letter_to_num("KFIT")
        a = solve_for_a(crib, ngram)  # 17
        print(solve_for_b(crib, ngram, a))  # 2

    if testing[8]:
        crib_affine(tests[3], "CRIB")  # 21, 5

    if testing[9]:
        mono_fitness_affine(tests[4])  # 7, 22

        transposed = mono_fitness_affine(tests[5])  # 9 ,2
        output = []
        for block in split_into_blocks(transposed, 3):
            output += list(reversed(block))
        print("".join(output))
