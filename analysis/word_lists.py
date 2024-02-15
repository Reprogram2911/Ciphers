import json
from collections import Counter

from ciphers.analysis.corpora import CORPUS_FP, get_file

WORDS_FP = get_file("words.txt")
WORDFREQ_FP = get_file("wordFreq.json")


def read_dict(fp):
    return json.load(fp)


def write_dict(dictionary, fp):
    json.dump(dictionary, fp, indent=0)


def alpha_word_list(text):
    words = text.split()
    words = list(set(words))  # removes duplicates
    return sorted(words)


def freq_word_list(text):
    words = text.split()
    freq = Counter(words)
    freq = freq.most_common()
    return dict(freq)


def analyse_words(source, alpha_dest=None, freq_dest=None):
    with open(source, "r") as f:
        text = f.read()

    if alpha_dest is not None:
        alpha_words = alpha_word_list(text)
        with open(alpha_dest, "w") as f:
            f.write("\n".join(alpha_words))

    if freq_dest is not None:
        freq_words = freq_word_list(text)
        with open(freq_dest, "w") as f:
            write_dict(freq_words, f)


if __name__ == "__main__":
    analyse_words(CORPUS_FP, WORDS_FP, WORDFREQ_FP)
