#!/usr/bin/python3
"""
Copyright © Morgan Leclerc and Catholic University of Louvain (2018)

morgan.leclerc@student.uclouvain.be

This software is governed by the CeCILL-B license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL-B
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL-B license and that you accept its terms.
"""

__author__ = 'Morgan Leclerc and Laurent Ziegler'
__doc__ = '''
This module is governed by the CeCILL-B license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL-B
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

This module aims at answering to a problem asked in a probability & statistics
course from the Polytechnic School of Louvain (LFSAB1105 Probability and 
Statistics, by Donatien Hainaut and Rainer Von Sachs). Whenever we reference a
book, it is the reference book of the course :
Mathematical statistics with applications. Wackerly, Mendenhall, Scheaffer.

This module provides functions to compute some basic quantities over 
arbitrary large samples, (like the mean, the variances, and quantiles) for 
single variable probabilities, to generate pseudo-random numbers following 
exponential and gamma distributions, and many plot and printing utilities.

This module needs Python 3.5+ to run
'''

############################
#     FOR OUR TEACHERS     #
############################
#        Group 37          #
# Morgan Leclerc  36071600 #
# Laurent Ziegler 00000000 #
# Raphael Goetz   00000000 #
#                 00000000 #
#                 00000000 #
#                          #
############################


import sys
import time
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

if sys.version_info < (3, 5):
    print('tg')


def workstation(mean: float, size: int=1):
    """
    :param mean: The mean time an item spend at this workstation.
    :param size: Size of the sample.
    :return: The time of an item spent at this workstation
    """
    # Following the inverse transform property of cumulative distribution
    # functions, we can generate pseudo random numbers following any
    # distribution from uniformly distributed pseudo-random numbers.
    return -mean * np.log(1 - np.random.random(size))


def assembly_line(mean: float, size: int=1):
    """
    :param mean: The mean time an item spend at each workstation.
    :param size: Size of the sample.
    :return: The total time an item took to be produced.
    """
    res = np.zeros(size)
    for i in range(size):
        res[i] = np.sum(workstation(mean, 5))
    return res


def produce(prod_time: float, mean: float) -> int:
    """
    :param prod_time: The total production time of the line (must be > 0).
    :param mean: The mean time an item spend at each workstation
    :return: The number of items produced.
    """
    count = -1
    while prod_time > 0:
        count += 1
        prod_time -= assembly_line(mean)
    return count


if __name__ == '__main__':
    n_trials = 100, 1000, 10000
    prod_times = 8*60,
    means = 1, 3, 6

    report = []

    for m in means:
        for p in prod_times:
            for n in n_trials:
                s_time = time.time()
                sample = [produce(p, m) for _ in range(n)]
                s_mean = stats.tmean(sample)
                s_variance = stats.variation(sample)
                report.append({'production time': p,
                               'number of trials': n,
                               'time taken': time.time() - s_time,
                               'samples': sample,
                               'expected mean': m,
                               'expected variance': 2,
                               'sample mean': s_mean,
                               'sample variance': s_variance,
                               })

    print(report)




