from ciphers.analysis import split_into_slices
from ciphers.monosub import decipher_affine, encipher_affine, mono_fitness_affine
from ciphers.polysub.vigenere import get_period


def base_periodic_affine(text, keys, encipher):
    period = len(keys)
    output = []
    for i, char in enumerate(text):
        key = keys[i % period]
        if encipher:
            new_char = encipher_affine(char, *key)
        else:
            new_char = decipher_affine(char, *key)
        output.append(new_char)
    return "".join(output)


def encipher_periodic_affine(plaintext, keys):
    return base_periodic_affine(plaintext, keys, True)


def decipher_periodic_affine(ciphertext, keys):
    return base_periodic_affine(ciphertext, keys, False)


def output_periodic_affine(ciphertext, keys):
    plaintext = decipher_periodic_affine(ciphertext, keys)
    print("Keys:", keys)
    print("Plaintext:", plaintext)


def periodic_attack_periodic_affine(ciphertext, period=None):
    if period is None:
        period = get_period(ciphertext)
    slices = split_into_slices(ciphertext, period)
    keys = []
    for s in slices:
        k = mono_fitness_affine(s, output=False)
        keys.append(k)
    output_periodic_affine(ciphertext, keys)
