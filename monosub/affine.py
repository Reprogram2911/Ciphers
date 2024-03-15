from functools import reduce

from ciphers.analysis import (
    ALPHABET,
    get_freq,
    mono_fitness,
    split_into_ngrams,
    tetra_fitness,
)
from ciphers.monosub.caesar import all_equal, letter_to_num
from ciphers.monosub.mono_sub import decipher_mono_sub, encipher_mono_sub


def gcd(*args):
    if len(args) > 2:
        return reduce(gcd, args)
    m, n = args
    while n != 0:
        m %= n
        m, n = n, m
    return m


def lcm(m, n):
    return int((m * n) / gcd(m, n))


def lcm_2(*args):
    original_nums = [*args]
    nums = original_nums.copy()
    while not all_equal(nums):
        lowest = min(nums)
        index = nums.index(lowest)
        nums[index] += original_nums[index]
    return nums[0]


def coprime(m, n):
    return gcd(m, n) == 1


def multiplicative_inverse(x, m=len(ALPHABET)):
    if not coprime(x, m):
        return False

    t, t_, r, r_ = 0, 1, m, x
    while r_ != 0:
        q = r // r_
        t, t_ = t_, t - q * t_
        r, r_ = r_, r - q * r_
    if t < 0:
        t += m
    return t


def valid_key_affine(a):
    return coprime(a, len(ALPHABET))


def generate_alphabet_affine(a, b):
    if not valid_key_affine(a):
        raise ValueError("Multiplier is not invertible")
    output = []
    for index, letter in enumerate(ALPHABET):
        new_index = (a * index + b) % len(ALPHABET)
        output.append(ALPHABET[new_index])
    return output


def encipher_affine(plaintext, a, b):
    key = generate_alphabet_affine(a, b)
    return encipher_mono_sub(plaintext, key)


def decipher_affine(ciphertext, a, b):
    key = generate_alphabet_affine(a, b)
    return decipher_mono_sub(ciphertext, key)


def atbash2(text):
    return encipher_affine(text, 25, 25)


def encipher_multiplicative(plaintext, a):
    return encipher_affine(plaintext, a, 0)


def decipher_multiplicative(plaintext, a):
    return decipher_affine(plaintext, a, 0)


def output_affine(ciphertext, a, b):
    plaintext = decipher_affine(ciphertext, a, b)
    print("Multiplier:", a)
    print("Shift:", b)
    print("Plaintext:", plaintext)
    return plaintext


def brute_force_affine(ciphertext):
    expected = get_freq(4)
    poss_texts = {
        (a, b): decipher_affine(ciphertext, a, b)
        for a in range(len(ALPHABET))
        for b in range(len(ALPHABET))
        if valid_key_affine(a)
    }
    fitnesses = {
        key: tetra_fitness(poss_text, expected) for key, poss_text in poss_texts.items()
    }
    a, b = max(fitnesses, key=fitnesses.get)
    output_affine(ciphertext, a, b)


def all_pairs(items):
    return [
        (items[i], items[j])
        for i in range(len(items))
        for j in range(i + 1, len(items))
    ]


def solve_for_a(coefficients, rhses):
    new_coefficients = sorted(coefficients, reverse=True)
    pairs = all_pairs(new_coefficients)
    for i, j in pairs:
        diff = i - j
        if valid_key_affine(diff):
            index_i = list(coefficients).index(i)
            index_j = list(coefficients).index(j)
            diff_rhs = rhses[index_i] - rhses[index_j]
            diff_rhs *= multiplicative_inverse(diff)
            return diff_rhs % len(ALPHABET)


def solve_for_b(coefficients, rhses, a):
    # coefficient * a + b = rhs
    return (rhses[0] - coefficients[0] * a) % len(ALPHABET)


def crib_affine(ciphertext, crib):
    n = len(crib)
    ngrams = split_into_ngrams(ciphertext, n)
    coefficients = letter_to_num(crib)
    found = False
    for ngram in ngrams:
        rhses = letter_to_num(ngram)
        a = solve_for_a(coefficients, rhses)
        b = solve_for_b(coefficients, rhses, a)
        if valid_key_affine(a) and encipher_affine(crib, a, b) == ngram:
            output_affine(ciphertext, a, b)
            found = True
            break
    if not found:
        print("Key not found with crib", crib)


def mono_fitness_affine(ciphertext):
    expected = get_freq(1)
    poss_texts = {
        (a, b): decipher_affine(ciphertext, a, b)
        for a in range(len(ALPHABET))
        for b in range(len(ALPHABET))
        if valid_key_affine(a)
    }
    fitnesses = {
        key: mono_fitness(poss_text, expected) for key, poss_text in poss_texts.items()
    }
    a, b = max(fitnesses, key=fitnesses.get)
    return output_affine(ciphertext, a, b)
