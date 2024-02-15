from collections import Counter
from math import log

import matplotlib.pyplot as plt

from ciphers.analysis.corpora import CORPUS_FP, get_file
from ciphers.analysis.word_lists import write_dict

MONOFREQ_FP = get_file("monoFreq.json")
TETRAFREQ_FP = get_file("tetraFreq.json")


def split_into_ngrams(text, n):
    return [text[i : i + n] for i in range(len(text) - n + 1)]


def split_into_blocks(text, n):
    return [text[i : i + n] for i in range(0, len(text) - n + 1, n)]


def ngram_frequencies(text, n, overlapping=True, divide=True):
    if overlapping:
        ngrams = split_into_ngrams(text, n)
    else:
        ngrams = split_into_blocks(text, n)
    freq = Counter(ngrams)
    freq = freq.most_common()
    freq = dict(freq)
    if divide:
        freq = {k: v / len(text) for k, v in freq.items()}
    return freq


def mono_frequencies(text):
    return ngram_frequencies(text, 1)


def tetra_frequencies(text, logarithm=False):
    freq = ngram_frequencies(text, 4)
    if logarithm:
        freq = {k: log(v) for k, v in freq.items()}
    return freq


def plot_dict(dictionary):
    names = list(dictionary.keys())
    values = list(dictionary.values())
    plt.bar(range(len(dictionary)), values, tick_label=names)
    plt.show()
    plt.close()


def analyse_frequencies(source, mono_dest=None, tetra_dest=None):
    with open(source, "r") as f:
        text = f.read().replace(" ", "")

    mono_freq = mono_frequencies(text)
    plot_dict(dict(sorted(mono_freq.items())))
    plot_dict(mono_freq)

    if mono_dest is not None:
        with open(mono_dest, "w") as f:
            write_dict(mono_freq, f)

    if tetra_dest is not None:
        tetra_freq = tetra_frequencies(text)
        with open(tetra_dest, "w") as f:
            write_dict(tetra_freq, f)


if __name__ == "__main__":
    analyse_frequencies(CORPUS_FP, MONOFREQ_FP, TETRAFREQ_FP)
