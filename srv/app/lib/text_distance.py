# -*- coding: utf-8 -*-
import textdistance
from .phonetize import translit
import re


def compute_distance(text1, text2, algorithm='damerau_levenshtein',
                     normalize=True, qval=1):

    algorithm = algorithm.lower()

    text1 = translit(text1) 
    text2 = translit(text2)

    def name_error():
        raise NameError('You have entered the wrong algorithm name.\n'
                        'Possible values: "hamming", "levenshtein", '
                        '"damerau_levenshtein" (default), "jaro", '
                        '"jaro_winkler", "gotoh", "smith_waterman"')

    return getattr(getattr(textdistance,
        'Hamming' if algorithm == 'hamming' else
        'Levenshtein' if algorithm == 'levenshtein' else
        'DamerauLevenshtein' if algorithm == 'damerau_levenshtein' else
        'Jaro' if algorithm == 'jaro' else
        'JaroWinkler' if algorithm == 'jaro_winkler' else
        'SmithWaterman' if algorithm == 'smith_waterman' else
        name_error()
    )(qval=qval), 'normalized_distance' if normalize else 'distance')(text1,
                                                                      text2)
