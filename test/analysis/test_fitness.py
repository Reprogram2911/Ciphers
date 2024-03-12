from random import choice, randint
from time import perf_counter

import matplotlib.pyplot as plt

from ciphers.analysis import ALPHABET, get_corpus, get_freq
from ciphers.analysis.fitness import (
    chi_squared,
    mono_fitness,
    mono_fitness_chi2,
    tetra_fitness,
)

CORPUS = get_corpus().replace(" ", "")


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
    num_times = 500
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
        print(f"{label} - On sublength {sublength} ({time_taken:.1f} secs)")
        if random:
            value = average_random(sublength, function, *args)
        else:
            value = average_corpus(sublength, function, *args)
        ys.append(value)
    xs = list(sublengths)
    plt.plot(xs, ys)
    plt.ylabel(label)
    if random:
        plt.xlabel("Length of random subtext")
    else:
        plt.xlabel("Length of subtext within corpus")
    plt.show()
    plt.close()


def test_fitness_function(function, n=1, random=False):
    expected = get_freq(n)
    test_function("Fitness", function, random, expected)


if __name__ == "__main__":
    testing = "0000"
    testing = [int(i) for i in testing]

    if testing[0]:
        print(chi_squared([1.1, 2.5, 7.3], [1, 3, 7]))

    if testing[1]:
        test_fitness_function(mono_fitness_chi2)  # -0.06
        test_fitness_function(mono_fitness)  # 0.98

    if testing[2]:
        test_fitness_function(tetra_fitness, 4)  # -9.6

    if testing[3]:
        test_fitness_function(mono_fitness_chi2, random=True)  # -5.0
        test_fitness_function(mono_fitness, random=True)  # 0.75
        test_fitness_function(tetra_fitness, 4, True)  # -14.7
