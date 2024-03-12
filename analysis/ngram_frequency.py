from collections import Counter
from math import log

import matplotlib.pyplot as plt

from ciphers.analysis.corpora import ALPHABET, CORPUS_FP, get_file, get_input, output
from ciphers.analysis.word_lists import dict_to_str, read_dict

MONOFREQ_FP = get_file("monoFreq.json")
TETRAFREQ_FP = get_file("tetraFreq.json")


def get_freq(n):
    match n:
        case 1:
            fp = MONOFREQ_FP
        case 4:
            fp = TETRAFREQ_FP
        case _:
            raise ValueError("Only 1-gram or 4-gram frequencies")
    return read_dict(fp)


def split_into_ngrams(text, n):
    return [text[i : i + n] for i in range(len(text) - n + 1)]


def split_into_blocks(text, n):
    return [text[i : i + n] for i in range(0, len(text) - n + 1, n)]


def ngram_frequencies(text, n, overlapping=True, divide=True, s=False):
    if overlapping:
        ngrams = split_into_ngrams(text, n)
    else:
        ngrams = split_into_blocks(text, n)
    freq = Counter(ngrams)
    freq = freq.most_common()
    freq = dict(freq)
    if divide:
        freq = {k: v / len(text) for k, v in freq.items()}
    if s:
        return dict_to_str(freq)
    return freq


def mono_frequencies(text, **kwargs):
    freq = ngram_frequencies(text, 1, **kwargs)
    if kwargs:
        for letter in ALPHABET:
            if letter not in freq:
                freq[letter] = 0
    return freq


def tetra_frequencies(text, logarithm=False, **kwargs):
    freq = ngram_frequencies(text, 4, **kwargs)
    if logarithm:
        freq = {k: log(v) for k, v in freq.items()}
    return freq


def plot_dict(dictionary):
    names = list(dictionary.keys())
    values = list(dictionary.values())
    plt.bar(range(len(dictionary)), values, tick_label=names)
    plt.show()
    plt.close()


def analyse_frequencies(source=None, mono_dest=None, tetra_dest=None, spaces=False):
    text = get_input(source)
    if not spaces:
        text = text.replace(" ", "")

    mono_freq = mono_frequencies(text)
    plot_dict(dict(sorted(mono_freq.items())))
    plot_dict(mono_freq)

    mono_s = mono_frequencies(text, s=True)
    output(mono_s, mono_dest)

    tetra_s = tetra_frequencies(text, s=True)
    output(tetra_s, tetra_dest)


if __name__ == "__main__":
    analyse_frequencies(CORPUS_FP, MONOFREQ_FP, TETRAFREQ_FP)
