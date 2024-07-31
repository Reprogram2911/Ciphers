from itertools import product

from ciphers.analysis import (
    ALPHABET,
    CUTOFF_TETRA_FITNESS,
    cos_angle,
    get_freq,
    get_words,
    mono_frequencies,
    split_into_slices,
    tetra_fitness,
)
from ciphers.monosub import (
    decipher_mono_sub,
    encipher_caesar,
    encipher_mono_sub,
    fill_key_1,
    hill_climbing_mono_sub,
    invert_key,
    num_to_letter,
)
from ciphers.polysub.vigenere import decipher_vigenere, get_period


def generate_quagmire_alphabets(k_alphabet, k_shifts, k_extra=None, version=1):
    match version:
        case 1:
            plaintext = fill_key_1(k_alphabet)
            changed = ALPHABET
            pos_a = plaintext.index(ALPHABET[0])
        case 2:
            plaintext = ALPHABET
            changed = fill_key_1(k_alphabet)
            pos_a = plaintext.index(ALPHABET[0])
        case 3:
            plaintext = fill_key_1(k_alphabet)
            changed = fill_key_1(k_alphabet)
            pos_a = 0
        case 4:
            plaintext = fill_key_1(k_alphabet)
            changed = fill_key_1(k_extra)
            pos_a = 0
    keys = []
    for k in k_shifts:
        pos_k = changed.index(k)
        key = changed[pos_k:] + changed[:pos_k]
        key = key[-pos_a:] + key[:-pos_a]
        zipped = zip(plaintext, key)
        key = "".join([x for _, x in sorted(zipped)])
        keys.append(key)
    return keys


def quagmire(encipher, text, k_alphabet, k_shifts, k_extra=None, version=1):
    keys = generate_quagmire_alphabets(k_alphabet, k_shifts, k_extra, version)
    period = len(keys)
    new_text = []
    for i, letter in enumerate(text):
        key = keys[i % period]
        if encipher:
            new_letter = encipher_mono_sub(letter, key)
        else:
            new_letter = decipher_mono_sub(letter, key)
        new_text.append(new_letter)
    return "".join(new_text)


def encipher_quagmire(plaintext, k_alphabet, k_shifts, k_extra=None, version=1):
    return quagmire(True, plaintext, k_alphabet, k_shifts, k_extra, version)


def decipher_quagmire(plaintext, k_alphabet, k_shifts, k_extra=None, version=1):
    return quagmire(False, plaintext, k_alphabet, k_shifts, k_extra, version)


def output_quagmire(ciphertext, k_alphabet, k_shifts, k_extra=None, version=1):
    plaintext = decipher_quagmire(ciphertext, k_alphabet, k_shifts, k_extra, version)
    print("Quagmire version:", version)
    print("Keyword 1:", k_alphabet)
    print("Keyword 2:", k_shifts)
    if k_extra is not None:
        print("Keyword 3:", k_extra)
    print("Plaintext:", plaintext)


def dictionary_quagmire(ciphertext, version, lim=100, period=None):
    if period is None:
        period = get_period(ciphertext)
    words = get_words()
    words = [w for w in words if len(w) == period][:lim]
    # period only restricts length of k_shifts
    expected = get_freq(4)
    highest_f = -500
    best_words = ["", ""]
    found = False
    for pair in product(words, repeat=2):
        pair = list(pair)
        # print(pair)
        poss_text = decipher_quagmire(ciphertext, *pair, version)
        fitness = tetra_fitness(poss_text, expected)
        if fitness > CUTOFF_TETRA_FITNESS:
            found = True
            break
        if fitness > highest_f:
            highest_f = fitness
            best_words = pair
            print(best_words)

    if not found:
        pair = best_words
        print("Dictionary attack failed; best found was:")

    output_quagmire(ciphertext, *pair, version=version)


def factor_quagmire_1(k_alphabet, k_shifts):
    keys = generate_quagmire_alphabets(k_alphabet, k_shifts, 1)
    monosub_key = keys[0]
    shift = (-ALPHABET.index(k_shifts[0])) % 26
    vigenere_key = encipher_caesar(k_shifts, shift)
    return monosub_key, vigenere_key


def factoring_quagmire_1_attack(ciphertext, period=None):
    if period is None:
        period = get_period(ciphertext)
    slices = split_into_slices(ciphertext, period)
    monofreqs = [
        list(dict(sorted(mono_frequencies(s).items())).values()) for s in slices
    ]
    sample = monofreqs[0]
    shifts = [0]
    for freq in monofreqs[1:]:
        highest_similarity = -500
        for i in range(len(freq)):
            test_freq = freq[i:] + freq[:i]
            similarity = cos_angle(test_freq, sample)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_shift = i
        shifts.append(best_shift)
    vig_key = num_to_letter(shifts)
    print(vig_key)
    pt1 = decipher_vigenere(ciphertext, vig_key)
    mono_key = hill_climbing_mono_sub(pt1, init_key="RWUXVYZATBCSDEFGQIJKLMNOPH")

    k_shifts = encipher_caesar(vig_key, ALPHABET.index(mono_key[0]))
    print(k_shifts)
    k_alpha = invert_key(mono_key)
    print(k_alpha)


def factor_quagmire_2(k_alphabet, k_shifts):
    monosub_key = fill_key_1(k_alphabet)
    vigenere_key = decipher_mono_sub(k_shifts, monosub_key)
    return monosub_key, vigenere_key


def factor_quagmire_3(k_alphabet, k_shifts):
    monosub2 = fill_key_1(k_alphabet)
    monosub1 = invert_key(monosub2)
    vig = encipher_mono_sub(k_shifts, monosub1)
    return monosub1, vig, monosub2


def factor_quagmire_4(k_alphabet, k_shifts, k_extra):
    monosub2 = fill_key_1(k_extra)
    monosub1 = invert_key(fill_key_1(k_alphabet))
    vig = decipher_mono_sub(k_shifts, monosub2)
    return monosub1, vig, monosub2
