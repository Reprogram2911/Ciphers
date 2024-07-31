from .corpora import ALPHABET, clean, get_corpus
from .fitness import (
    CUTOFF_TETRA_FITNESS,
    EXPECTED_MONO_FITNESS,
    EXPECTED_TETRA_FITNESS,
    chi_squared,
    cos_angle,
    mono_fitness,
    mono_fitness_chi2,
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
from .randomness import (
    EXPECTED_IOC,
    find_period_auto,
    ioc,
    plot_period_graph,
    similar_ioc,
    split_into_slices,
)
from .word_lists import WORDS_FP, dict_to_str, get_words, read_dict
