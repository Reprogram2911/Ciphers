from math import log

import matplotlib.pyplot as plt

from ciphers.analysis.ngram_frequency import ngram_frequencies, mono_frequencies


def ioc(text, n=1):
    length = len(text)
    freqs = ngram_frequencies(text, n, overlapping=False).values()
    freqs = [freq * (length - n + 1) for freq in freqs]
    total = 0
    for freq in freqs:
        numerator = freq * (freq - 1)
        total += numerator
    denominator = length * (length - 1)
    total /= denominator
    return total * 26**n


def entropy(text):
    mono_freq = mono_frequencies(text)
    freqs = list(mono_freq.values())
    freqs = [freq * log(freq, 26) for freq in freqs]
    total = sum(freqs)
    return -total


def split_into_slices(text, period):
    slices = [[] for _ in range(period)]
    for index, letter in enumerate(text):
        slices[index % period].append(letter)
    return ["".join(slice) for slice in slices]


def find_block_size(text):
    iocs = []
    max_period = 30
    periods = range(1, max_period + 1)
    for period in periods:
        slices = split_into_slices(text, period)
        total = 0
        for slice in slices:
            total += ioc(slice)
        average = total / len(slices)
        iocs.append(average)
    f, ax = plt.subplots(1)
    xs = list(periods)
    ys = iocs
    ax.bar(xs, ys)
    ax.set_ylim(ymin=1.0)
    plt.axhline(y=1.73, color="b", linestyle="--")
    plt.xlabel("Period")
    plt.ylabel("IoC")
    plt.show()
    plt.close()
