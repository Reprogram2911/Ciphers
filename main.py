from ciphers.analysis import clean
from ciphers.monosub import (
    brute_force_affine,
    brute_force_caesar,
    dictionary_keyword,
    hill_climbing_mono_sub,
    mono_sub_likely,
)


def get_input():
    print("Enter your text: ")
    return clean(input())


def get_confirmation():
    print("Does this look like English? (y/n)")
    match input().lower():
        case "y":
            return True
        case "n":
            return False


def mono_sub_attacks(text):
    print("Trying caesar attack:")
    brute_force_caesar(text)
    if get_confirmation():
        return
    print("Trying affine attack:")
    brute_force_affine(text)
    if get_confirmation():
        return
    print("Trying keyword attack:")
    dictionary_keyword(text)
    if get_confirmation():
        return
    print("Trying hill climbing attack:")
    hill_climbing_mono_sub(text)


def analyse():
    text = get_input()
    if mono_sub_likely(text):
        print("Identified as a monoalphabetic substitution")
        mono_sub_attacks(text)


if __name__ == "__main__":
    analyse()
