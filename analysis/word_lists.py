import json
from collections import Counter

from ciphers.analysis.corpora import get_file, CORPUS_FP, get_input, output, strip

WORDS_FP = get_file("words.txt")
WORDFREQ_FP = get_file("wordFreq.json")


def read_dict(fp):
    return json.load(fp)


def dict_to_str(dictionary):
    return json.dumps(dictionary, indent=0)


def alpha_word_list(text, s=False):
    words = text.split()
    words = list(set(words))  # removes duplicates
    words = sorted(words)
    if s:
        return "\n".join(words)
    return words


def freq_word_list(text, s=False):
    words = text.split()
    freq = Counter(words)
    freq = freq.most_common()
    freq = dict(freq)
    if s:
        return dict_to_str(freq)
    return freq


def analyse_words(source=None, alpha_dest=None, freq_dest=None):
    text = get_input(source)
    text = strip(text)

    alpha_s = alpha_word_list(text, True)
    output(alpha_s, alpha_dest)

    freq_s = freq_word_list(text, True)
    output(freq_s, freq_dest)


if __name__ == "__main__":
    analyse_words(CORPUS_FP, WORDS_FP, WORDFREQ_FP)
