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
Statistics, by Donatien Hainaut and Rainer Von Sachs).

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


def produce(prod_time: float, man_mean: float, rep_mean: float=0) -> int:
    """
    Sample from a pseudo-random variable that represents the number of item
    produced by an assembly line over a given time.

    :param prod_time: The total production time of the line (must be > 0).
    :param man_mean: The mean time an item spend at each workstation
    :param rep_mean: The mean time needed to repair the line (0 to disactive
        line breakdown).
    :return: The number of items produced.
    """
    count = -1

    if np.random.random() < 0.1:
        # In case of breakdown, take time to repair the line
        prod_time -= -rep_mean * np.log(np.random.random())

    while prod_time > 0:
        count += 1
        # Time spent by going through 5 workstations in the assembly line
        prod_time -= np.sum(-man_mean * np.log(np.random.random(5)))
    return count


if __name__ == '__main__':
    # Output config
    histograms_plotting = True
    plots_title = False
    save_plots_fig = True
    summary_printing = True

    # Simulation config
    n_trials = 1e2, 1e3, 1e4,
    prod_times = 8 * 60,
    means = 3,

    report = []

    for m in means:
        for p in prod_times:
            for n in n_trials:
                n = int(n)
                s_time = time.time()

                # Generate sample
                sample = [produce(p, m, 0) for _ in range(n)]

                # Compute quantiles
                sample.sort()
                length = len(sample)
                lower_q = sample[int(0.05 * length)]
                higher_q = sample[int(0.95 * length)]

                # Compute mean and variance
                s_mean = stats.tmean(sample)
                s_variance = stats.variation(sample)

                # Generate report
                report.append({'production time': p,
                               'number of trials': n,
                               'time taken (s)': time.time() - s_time,
                               'expected mean': p / (5 * m),
                               'expected variance': '0.064',
                               'sample mean': s_mean,
                               'sample variance': s_variance,
                               '5% percentile': lower_q,
                               '95% percentile': higher_q,
                               })

                # Plots
                if histograms_plotting or save_plots_fig:
                    plt.hist(sample, range(0, 50), density=True)

                    if plots_title:
                        plt.title(
                            'Sample density histogram $\mu={}$ $p={}$ $n={}$'
                            .format(m, p, n))

                    if save_plots_fig:
                        plt.savefig('m3-p480-n1e{}_plot.png'
                                    .format(int(np.log10(n))))

                    if histograms_plotting:
                        plt.show()

    # Parse reports
    parse_summary(report, summary_printing)
