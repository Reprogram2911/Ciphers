from .corpora import ALPHABET, get_corpus, strip
from .fitness import (
    fitness,
    mono_fitness,
    mono_fitness_chi2,
    mono_fitness_cos,
    tetra_fitness,
)
from .ngram_frequency import (
    analyse_frequencies,
    get_freq,
    mono_frequencies,
    ngram_frequencies,
    plot_dict,
    split_into_blocks,
    split_into_ngrams,
)
from .randomness import find_block_size, ioc, split_into_slices
from .word_lists import WORDFREQ_FP, WORDS_FP, dict_to_str, read_dict
