from .corpora import ALPHABET, strip, get_corpus
from .fitness import mono_fitness, tetra_fitness, mono_fitness_chi2, mono_fitness_cos
from .ngram_frequency import (
    mono_frequencies,
    ngram_frequencies,
    split_into_ngrams,
    get_freq,
)
from .randomness import ioc
from .word_lists import read_dict, dict_to_str
