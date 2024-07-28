from math import log

import matplotlib.pyplot as plt
import numpy as np

from ciphers.analysis import ALPHABET
from ciphers.analysis.ngram_frequency import mono_frequencies, ngram_frequencies
from ciphers.test.analysis.test_fitness import average_corpus

EXPECTED_IOC = 1.73
EXPECTED_IOCS = [EXPECTED_IOC, 1.33, 3.4, 16, 130, 1200]
EXPECTED_ENTROPY = 0.88

RANDOM_IOC = 1.00
RANDOM_ENTROPY = 0.99

SD_IOC = 0.15


def ioc(text, n=1):
    length = len(text)
    assert length > 1
    freqs = ngram_frequencies(text, n, overlapping=False).values()
    freqs = np.array(list(freqs))
    freqs *= length - n + 1
    numerator = freqs * (freqs - 1)
    total = numerator.sum()
    denominator = length * (length - 1)
    total /= denominator
    return total * len(ALPHABET) ** n


def entropy(text):
    mono_freq = mono_frequencies(text)
    freqs = list(mono_freq.values())

    freqs = [freq * log(freq, len(ALPHABET)) for freq in freqs]
    total = sum(freqs)
    return -total


def split_into_slices(text, period):
    slices = [[] for _ in range(period)]
    for index, letter in enumerate(text):
        slices[index % period].append(letter)
    return ["".join(s) for s in slices]


def similar_ioc(text=None, ioc_v=None):
    if text is None:
        assert ioc_v is not None
        actual_ioc = ioc_v
    else:
        actual_ioc = ioc(text)
    return abs(actual_ioc - EXPECTED_IOC) < SD_IOC or actual_ioc > EXPECTED_IOC


def find_period_auto(text):
    max_period = 10
    period = 1
    avgs = []
    while period <= max_period:
        slices = split_into_slices(text, period)
        total = 0
        for s in slices:
            total += ioc(s)
        average = total / period
        avgs.append(average)
        period += 1
    plt.plot([i + 1 for i in range(max_period)], avgs)
    plt.show()
    plt.close()
    plot_period_graph(text)
    return input_number(f"Give keyword length (optimal m=): ")


def input_number(message=None):
    valid_input = False
    while not valid_input:
        user_input = input(message)
        if user_input.isdigit():
            valid_input = True
    return user_input


def plot_period_graph(text):
    iocs = []
    max_period = min(30, len(text) // 2)
    periods = range(1, max_period + 1)
    for period in periods:
        slices = split_into_slices(text, period)
        total = 0
        for s in slices:
            total += ioc(s)
        average = total / period
        iocs.append(average)
    f, ax = plt.subplots(1)
    xs = list(periods)
    ys = iocs
    ax.bar(xs, ys)
    plt.xticks(periods[1::2])
    ax.set_ylim(ymin=1.0)
    plt.axhline(y=EXPECTED_IOC, color="b", linestyle="--")
    plt.xlabel("Period")
    plt.ylabel("IoC")
    plt.show()
    plt.close()


def percentage_error(value, expected):
    return abs((value - expected) / expected) * 100


def find_block_size(text):
    length = len(text)
    for n in range(2, 7):
        actual = ioc(text, n)
        expected = average_corpus(length, ioc, n)
        print(f"IoC {n}: {percentage_error(actual, expected):.2f}")
