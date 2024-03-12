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


def clean(text):
    text = text.upper()
    included = ALPHABET + string.whitespace
    text = [character for character in text if character in included]
    text = "".join(text)
    return standardise_whitespace(text)


def get_input(source):
    if source is None:
        print("Input:")
        text = input()
    elif Path(source).suffix == ".txt":
        with open(source, "r") as f:
            text = f.read()
    else:
        text = source
    return clean(text)


def output(text, destination):
    if destination is None:
        print("Output:")
        print(text)
    else:
        with open(destination, "w") as f:
            f.write(text)


def perform_function(function, source=None, destination=None):
    argument = get_input(source)
    result = function(argument)
    output(result, destination)


if __name__ == "__main__":
    perform_function(clean, get_file("brownCorpus.txt"), CORPUS_FP)
    # Brown corpus sourced from http://www.sls.hawaii.edu/bley-vroman/brown.txt
