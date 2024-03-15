from math import log, sqrt

import numpy as np

from ciphers.analysis.ngram_frequency import mono_frequencies, split_into_ngrams

EXPECTED_MONO_FITNESS = 0.98
EXPECTED_MONO_FITNESS_CHI2 = -0.06
EXPECTED_TETRA_FITNESS = -9.6

RANDOM_MONO_FITNESS = 0.75
RANDOM_MONO_FITNESS_CHI2 = -5.0
RANDOM_TETRA_FITNESS = -14.7

CUTOFF_TETRA_FITNESS = -10


def chi_squared(measured, expected):
    measured = np.array(measured)
    expected = np.array(expected)
    numerator = (measured - expected) ** 2
    total = numerator / expected
    return total.sum()


def chi_squared_2(measured, expected):
    total = 0
    for m, e in zip(measured, expected):
        numerator = (m - e) ** 2
        total += numerator / e
    return total


def mono_fitness_chi2(text, expected):
    measured = mono_frequencies(text)
    m_list = []
    e_list = []
    for k, v_m in measured.items():
        if k in expected:
            v_e = expected[k]
            m_list.append(v_m)
            e_list.append(v_e)
    return -chi_squared(m_list, e_list)


def dot_product(u, v):
    if len(u) != len(v):
        raise ValueError("The dimensions of the two vectors do not match")
    return np.dot(u, v)


def dot_product_2(u, v):
    if len(u) != len(v):
        raise ValueError("The dimensions of the two vectors do not match")
    products = [a * b for a, b in zip(u, v)]
    return sum(products)


def cos_angle(u, v):
    numerator = dot_product(u, v)
    denominator = sqrt(dot_product(u, u) * dot_product(v, v))
    return numerator / denominator


def mono_fitness(text, expected):
    measured = mono_frequencies(text)
    m_list, e_list = [], []
    for k, v_m in measured.items():
        if k in expected:
            v_e = expected[k]
            m_list.append(v_m), e_list.append(v_e)
    return cos_angle(m_list, e_list)


def tetra_fitness(text, expected):
    total = 0
    tetragrams = split_into_ngrams(text, 4)
    for tetragram in tetragrams:
        f = expected.get(tetragram, 0)
        if f != 0:
            total += log(f)
        else:
            total -= 15
    return total / (len(text) - 3)
