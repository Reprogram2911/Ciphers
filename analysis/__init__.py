from .corpora import ALPHABET, get_corpus, strip
from .fitness import mono_fitness, mono_fitness_chi2, mono_fitness_cos, tetra_fitness
from .ngram_frequency import (
    analyse_frequencies,
    get_freq,
    mono_frequencies,
    ngram_frequencies,
    split_into_blocks,
    split_into_ngrams,
)
from .randomness import ioc
from .word_lists import dict_to_str, read_dict
