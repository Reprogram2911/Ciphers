import string
from pathlib import Path


ALPHABET = string.ascii_uppercase


def get_file(filename):
    return Path(__file__).parents[1] / "files" / filename


CORPUS_FP = get_file("corpus.txt")


def standardise_whitespace(text):
    words = text.split()
    return " ".join(words)


def strip(text):
    text = text.upper()
    included = ALPHABET + string.whitespace
    text = [character for character in text if character in included]
    text = "".join(text)
    return standardise_whitespace(text)


def function_on_file(function, source, destination):
    with open(source, "r") as f:
        arg = f.read()

    result = function(arg)

    with open(destination, "w") as f:
        f.write(result)


if __name__ == "__main__":
    function_on_file(strip, get_file("brownCorpus.txt"), CORPUS_FP)
    # Brown corpus sourced from http://www.sls.hawaii.edu/bley-vroman/brown.txt
