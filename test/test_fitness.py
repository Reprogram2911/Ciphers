from random import randint, choice
from time import perf_counter

import matplotlib.pyplot as plt

from ciphers.analysis import CORPUS_FP, MONOFREQ_FP, TETRAFREQ_FP, read_dict, ALPHABET
from ciphers.analysis.fitness import (
    chi_squared,
    mono_fitness_chi2,
    mono_fitness_cos,
    tetra_fitness,
)

with open(CORPUS_FP, "r") as f:
    CORPUS = f.read().replace(" ", "")


def average_corpus(sublength, function, *args):
    length = len(CORPUS)
    num_times = 1000
    total = 0
    for _ in range(num_times):
        index = randint(0, length - sublength)
        subtext = CORPUS[index : index + sublength]
        total += function(subtext, *args)
    return total / num_times


def average_random(sublength, function, *args):
    num_times = 100
    total = 0
    for _ in range(num_times):
        subtext = "".join(choice(ALPHABET) for _ in range(sublength))
        total += function(subtext, *args)
    return total / num_times


def test_function(label, function, random, *args):
    sublengths = range(500, 1000, 5)
    ys = []
    start_time = perf_counter()
    for sublength in sublengths:
        time_taken = perf_counter() - start_time
        print(f"{label}\tOn sublength {sublength} ({time_taken:.1f} secs)")
        if random:
            value = average_random(sublength, function, *args)
        else:
            value = average_corpus(sublength, function, *args)
        ys.append(value)
    xs = list(sublengths)
    plt.bar(xs, ys)
    plt.ylabel(label)
    if random:
        plt.xlabel("Length of random subtext")
    else:
        plt.xlabel("Length of subtext within corpus")
    plt.show()
    plt.close()


def test_fitness_function(function, n=1, random=False):
    filenames = {1: MONOFREQ_FP, 4: TETRAFREQ_FP}
    filename = filenames[n]
    with open(filename, "r") as f:
        expected = read_dict(f)
    test_function("Fitness", function, random, expected)


if __name__ == "__main__":
    testing = "0000"
    testing = [int(i) for i in testing]

    if testing[0]:
        print(chi_squared([1.1, 2.5, 7.3], [1, 3, 7]))

    if testing[1]:
        test_fitness_function(mono_fitness_chi2)  # -0.06
        test_fitness_function(mono_fitness_cos)  # 0.98

    if testing[2]:
        test_fitness_function(tetra_fitness, 4)  # -9.6

    if testing[3]:
        test_fitness_function(mono_fitness_chi2, random=True)  # -5
        test_fitness_function(mono_fitness_cos, random=True)  # 0.75
        test_fitness_function(tetra_fitness, 4, True)  # -14.7
