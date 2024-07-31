from itertools import product
from time import perf_counter

from ciphers.analysis import (
    ALPHABET,
    CUTOFF_TETRA_FITNESS,
    clean,
    get_freq,
    get_words,
    tetra_fitness,
)
from ciphers.monosub import encipher_mono_sub
from ciphers.polysub import encipher_vigenere
from ciphers.polysub.quagmire import (
    decipher_quagmire,
    dictionary_quagmire,
    encipher_quagmire,
    factor_quagmire_1,
    factor_quagmire_2,
    factor_quagmire_3,
    factor_quagmire_4,
    factoring_quagmire_1_attack,
    output_quagmire,
)
from ciphers.test.utils import get_tests


def repunctuate(plaintext, ciphertext):
    ciphertext = list(ciphertext)
    for i, pt_letter in enumerate(plaintext):
        if pt_letter not in ALPHABET:
            ciphertext.insert(i, pt_letter)
    return "".join(ciphertext)


if __name__ == "__main__":
    testing = "00000000000000000"
    testing = [int(i) for i in testing]

    tests = get_tests("testQuagmire.txt")
    tests = [clean(test).replace(" ", "") for test in tests]

    if testing[0]:
        plaintext = tests[0]
        ks = ["QUAGMIRE", "CIPHER"]
        target = "USSY GWTZPIJ UT NDOINSAUP YUUS P FDRDKSLJ YFYZMI".replace(" ", "")

        ciphertext = encipher_quagmire(plaintext, *ks, version=1)
        print(ciphertext)
        assert ciphertext == target

        mono, vig = factor_quagmire_1(*ks)
        ct1 = encipher_mono_sub(plaintext, mono)
        ct2 = encipher_vigenere(ct1, vig)
        print(ct2)
        assert ct2 == target

    if testing[1]:
        ciphertext = encipher_quagmire(tests[1], "ULTIMATE", "QUESTION", version=1)
        print(ciphertext)

    if testing[2]:
        plaintext = decipher_quagmire(tests[2], "WAR", "PEACE", version=1)
        print(plaintext)

    if testing[3]:
        dictionary_quagmire(tests[3], 1, 100, period=5)
        # BEGAN VOICE

    if testing[4]:
        ciphertext = tests[4]
        factoring_quagmire_1_attack(ciphertext, period=10)
        # RWUXVYZATBCSDEFGQIJKLMNOPH
        # k_shifts: RABBITHOLE
        # k_alpha: HJKMNOPZRSTUVWXYQALICEBDFG
        #          HJKMNOPQRSTUVWXYZALICEBDFG
        # -> ALICE
        print(decipher_quagmire(ciphertext, "ALICE", "RABBITHOLE", version=1))

    if testing[5]:
        plaintext = tests[5]
        ks = ["QUAGMIRE", "CIPHER"]
        target = "AHQM SDUXPPF KU CIKYMYYWL GKAH P AURLOQGF BOTZNY".replace(" ", "")

        ciphertext = encipher_quagmire(plaintext, *ks, version=2)
        print(ciphertext)
        assert ciphertext == target

        mono, vig = factor_quagmire_2(*ks)
        print(mono, vig)
        ct1 = encipher_vigenere(plaintext, vig)
        ct2 = encipher_mono_sub(ct1, mono)
        print(ct2)
        assert ct2 == target

    if testing[6]:
        ciphertext = encipher_quagmire(tests[6], "CHARLES", "DICKENS", version=2)
        print(ciphertext)

    if testing[7]:
        plaintext = decipher_quagmire(tests[7], "PLANET", "EARTH", version=2)
        print(plaintext)

    if testing[8]:
        ciphertext = tests[7]
        period = 5
        lim = 300
        version = 2
        start = perf_counter()
        words = get_words()
        words = [w for w in words if len(w) == period][:lim]
        print(" ".join(words))

        # word_2s = [w for w in words if w.endswith("OWN")]
        expected = get_freq(4)
        highest_f = -500
        best_words = ["", ""]
        found = False
        old = "WHICH"
        c = 0
        for pair in product(words, repeat=2):
            pair = list(pair)
            if pair[0] != old:
                old = pair[0]
                c += 1
                print(c)
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
            words = best_words
            print("Dictionary attack failed; best found was:")

        output_quagmire(ciphertext, *words, version)
        end = perf_counter()
        delta = end - start
        print(f"{delta:.2f} seconds")
        # TAKEN EARTH, 202 seconds, lim = 200
        # TAKEN EARTH, 435 seconds, lim = 300
        # failed

    if testing[9]:
        plaintext = tests[5]
        ks = ["QUAGMIRE", "CIPHER"]
        target = "GOXI FJAYTLK FA HBVJMUZZW GFGO T HBBHCXPK LKXMSJ".replace(" ", "")

        ciphertext = encipher_quagmire(plaintext, *ks, version=3)
        print(ciphertext)
        assert ciphertext == target

        m1, v, m2 = factor_quagmire_3(*ks)
        print(m1, v, m2)
        ct1 = encipher_mono_sub(plaintext, m1)
        ct2 = encipher_vigenere(ct1, v)
        ct3 = encipher_mono_sub(ct2, m2)
        print(ct3)
        assert ct3 == target

    if testing[10]:
        plaintext = tests[10]
        ks = ["NURSERY", "RHYME"]
        ciphertext = encipher_quagmire(plaintext, *ks, version=3)
        print(ciphertext)

    if testing[11]:
        ciphertext = tests[11]
        ks = ["DOLPHINS", "FISHBOWL"]
        plaintext = decipher_quagmire(ciphertext, *ks, version=3)
        print(plaintext)

    if testing[12]:
        ciphertext = tests[12]
        dictionary_quagmire(ciphertext, 3, period=5)
        # THING, OTHER

    if testing[13]:
        plaintext = tests[5]
        ks = ["QUAGMIRE", "CIPHER", "KEYWORD"]
        target = "WZVR RHYDSLB FY SBTAWEAZU VFWZ S HYAHNVPB JJROQA".replace(" ", "")

        ciphertext = encipher_quagmire(plaintext, *ks, version=4)
        print(ciphertext)
        assert ciphertext == target

        m1, v, m2 = factor_quagmire_4(*ks)
        print(m1, v, m2)
        ct1 = encipher_mono_sub(plaintext, m1)
        ct2 = encipher_vigenere(ct1, v)
        ct3 = encipher_mono_sub(ct2, m2)
        print(ct3)
        assert ct3 == target

    if testing[14]:
        plaintext = tests[14]
        ks = ["FOUR", "WORD", "LETTER"]
        ciphertext = encipher_quagmire(plaintext, *ks, version=4)
        print(ciphertext)

    if testing[15]:
        ciphertext = tests[15]
        ks = ["FOUR", "COLOR", "PIGMENT"]
        plaintext = decipher_quagmire(ciphertext, *ks, version=4)
        print(plaintext)

    if testing[16]:
        ciphertext = tests[16]
        period = 5
        lim = 50
        version = 4

        words = get_words()
        words = [w for w in words if len(w) == period][:lim]
        print(" ".join(words))
        expected = get_freq(4)
        highest_f = -500
        best_words = ["", ""]
        found = False
        old = "WHICH"
        c = 0
        for triple in product(words, repeat=3):
            triple = list(triple)
            if triple[0] != old:
                old = triple[0]
                c += 1
                print(c)
            # print(pair)
            poss_text = decipher_quagmire(ciphertext, *triple, version)
            fitness = tetra_fitness(poss_text, expected)
            if fitness > CUTOFF_TETRA_FITNESS:
                found = True
                break
            if fitness > highest_f:
                highest_f = fitness
                best_words = triple
                print(best_words)

        if not found:
            words = best_words
            print("Dictionary attack failed; best found was:")

        output_quagmire(ciphertext, *words, version)

        # BEING THEIR STATE
        # THESE MIGHT PLACE
        # failed
