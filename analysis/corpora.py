from pathlib import Path
import string

ALPHABET = string.ascii_uppercase


def get_file(filename):
    return Path(__file__).parents[1] / "files" / filename


CORPUS_FP = get_file("corpus.txt")


def get_corpus():
    with open(CORPUS_FP, "r") as f:
        return f.read()


def standardise_whitespace(text):
    words = text.split()
    return " ".join(words)


def strip(text):
    text = text.upper()
    included = ALPHABET + string.whitespace
    text = [character for character in text if character in included]
    text = "".join(text)
    return standardise_whitespace(text)


def get_input(source):
    if source is None:
        print("Input:")
        return input()

    if source.endswith(".txt"):
        with open(source, "r") as f:
            return f.read()

    return source


def output(s, dest):
    if dest is None:
        print("Output:")
        print(s)
    else:
        with open(dest, "w") as f:
            f.write(s)


def perform_function(function, source=None, destination=None):
    arg = get_input(source)
    result = function(arg)
    output(result, destination)


if __name__ == "__main__":
    perform_function(strip, get_file("brownCorpus.txt"), CORPUS_FP)
    # Brown corpus sourced from http://www.sls.hawaii.edu/bley-vroman/brown.txt
