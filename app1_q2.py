#!/usr/bin/python3
"""
Copyright © Morgan Leclerc, Laurent Ziegler, Catholic University of Louvain
(2018)

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

This module needs Python 3.5+ to run
'''


import sys
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from nice_parsers import parse_summary

if sys.version_info < (3, 5):
    print('This scrip needs python3.5+ to run')
    exit(0)


def get_price(mean: np.ndarray=1, variance: np.ndarray=1, alpha: np.ndarray=1,
              k: float=0, size: int=1) -> np.ndarray:
    """
    Generates a price for an option that promises the payment of the positive
    difference max(((Si)^αi − K),0) in one year, where Si is a vector of
    log-normal correlated random variables, and αi a vector of scalar.

    :param mean: The means of the random variables S, as a vector of size N.
    :param variance: The variances of the random variables S, as a N by N
        matrix.
    :param alpha: The vector of scalar α.
    :param k: The constant K.
    :param size: The number of price to generate.
    :return: The prices of the option in an array, equal to the expected
        cash-flows.
    """
    alpha = alpha*np.ones((size, 1))
    # Generating S1 x S2 x ... x Sn as log-normal correlated variables
    res = np.exp(np.random.multivariate_normal(mean, variance, size))
    res = np.max(np.power(res, alpha), axis=-1).flatten() - k
    return res


if __name__ == '__main__':
    # Output config
    histograms_plotting = True
    plots_title = False
    save_plots_fig = True
    summary_printing = True

    # Simulation config
    n_trials = 1e2, 1e3, 1e4, 1e6
    m = np.array([4.15, 2.39])
    v = np.array([[0.2*0.2, 0.2*0.25*0.85],
                  [0.2*0.25*0.85, 0.25*0.25]])
    a = np.array([1, 1])

    report = []

    for n in n_trials:
        n = int(n)
        s_time = time.time()

        # Generate sample
        sample = get_price(m, v, a, 682, n)

        # Compute quantiles
        sample.sort()
        length = len(sample)
        lower_q = sample[int(0.05 * length)]
        higher_q = sample[int(0.95 * length)]

        # Compute mean and variance
        s_mean = stats.tmean(sample)
        s_variance = stats.variation(sample)

        # Generate report
        report.append({'number of trials': n,
                       'time taken (s)': time.time() - s_time,
                       'expected mean': '??',
                       'expected variance': '??',
                       'sample mean': s_mean,
                       'sample variance': s_variance,
                       '5% percentile': lower_q,
                       '95% percentile': higher_q,
                       })

        # Plots
        if histograms_plotting or save_plots_fig:
            plt.hist(sample, np.linspace(-700, -500, min(100, int(np.sqrt(n)))),
                     density=True)

            if plots_title:
                plt.title('Sample density histogram $n={}$'.format(n))

            if save_plots_fig:
                plt.savefig('q2-3_n1e{}_plot.png'.format(len(str(n))-1))

            if histograms_plotting:
                plt.show()

    # Parse reports
    parse_summary(report, summary_printing)
