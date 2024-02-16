from ciphers.analysis import ALPHABET, get_freq, tetra_fitness
from ciphers.monosub.caesar import all_equal
from ciphers.monosub.mono_sub import encipher_mono_sub, decipher_mono_sub


def gcd(m, n):
    while n != 0:
        m %= n
        m, n = n, m
    return m


def lcm(m, n):
    return int((m * n) / gcd(m, n))


def lcm2(*args):
    original_nums = [*args]
    nums = original_nums.copy()
    while not all_equal(nums):
        lowest = min(nums)
        index = nums.index(lowest)
        nums[index] += original_nums[index]
    return nums[0]


def coprime(m, n):
    return gcd(m, n) == 1


def multiplicative_inverse(x, m):
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
    return coprime(a, 26)


def generate_alphabet_affine(a, b):
    if not valid_key_affine(a):
        raise ValueError("Multiplier is not invertible")
    output = []
    for index, letter in enumerate(ALPHABET):
        new_index = (a * index + b) % 26
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
    key = generate_alphabet_affine(a, 0)
    return encipher_mono_sub(plaintext, key)


def decipher_multiplicative(plaintext, a):
    key = generate_alphabet_affine(a, 0)
    return decipher_mono_sub(plaintext, key)


def output_affine(ciphertext, a, b):
    plaintext = decipher_affine(ciphertext, a, b)
    print("Multiplier:", a)
    print("Shift:", b)
    print("Plaintext:", plaintext)


def brute_force_affine(ciphertext):
    expected = get_freq(4)
    poss_texts = {
        (a, b): decipher_affine(ciphertext, a, b)
        for a in range(26)
        for b in range(26)
        if valid_key_affine(a)
    }
    fitnesses = {
        key: tetra_fitness(poss_text, expected) for key, poss_text in poss_texts.items()
    }
    a, b = max(fitnesses, key=fitnesses.get)
    output_affine(ciphertext, a, b)
