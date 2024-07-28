from collections import Counter
import json

from ciphers.analysis.corpora import CORPUS_FP, get_file, get_input, output

WORDS_FP = get_file("words.json")


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


def dict_to_str(d):
    return json.dumps(d, indent=0)


def str_to_dict(s):
    return json.loads(s)


def read_dict(fp):
    with open(fp, "r") as f:
        return str_to_dict(f.read())


def get_words():
    return list(read_dict(WORDS_FP).keys())


def analyse_words(source=None, alpha_dest=None, freq_dest=None):
    text = get_input(source)

    alpha_s = alpha_word_list(text, s=True)
    output(alpha_s, alpha_dest)

    freq_s = freq_word_list(text, s=True)
    output(freq_s, freq_dest)


if __name__ == "__main__":
    analyse_words(CORPUS_FP, None, WORDS_FP)
