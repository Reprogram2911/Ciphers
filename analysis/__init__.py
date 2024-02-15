from .corpora import ALPHABET, CORPUS_FP, strip
from .fitness import mono_fitness, tetra_fitness, mono_fitness_chi2, mono_fitness_cos
from .ngram_frequency import (
    mono_frequencies,
    ngram_frequencies,
    split_into_ngrams,
    MONOFREQ_FP,
    TETRAFREQ_FP,
)
from .randomness import ioc
from .word_lists import read_dict, write_dict
