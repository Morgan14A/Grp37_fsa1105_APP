#!/usr/bin/python3
"""
Copyright © Morgan Leclerc & Catholic University of Louvain (2018)

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

This program needs Python 3.5+ to run
"""

__author__ = 'Morgan Leclerc'
__doc__ = '''
No documentation for now, sorry.
Please see code comments, or send an email for any qestion you may have.
'''

###########################
#    FOR OUR TEACHERS     #
###########################
#       Group 37          #
# Morgan Leclerc 36071600 #
#                         #
###########################


import sys
# from itertools import product
import numpy as np
# import matplotlib.pyplot as plt


def get_mean_variance(data: np.ndarray):
    """
    Computes the mean and the variance of a numpy array using Welford's method.

    :param data: The array.
    :return: A 2-tuple of the mean, variance.
    """
    data = data.flatten()
    old_mean = new_mean = data[0]
    variance = count = 0
    for value in data:
        count += 1
        new_mean = old_mean + (value-old_mean)/count
        variance += (value-old_mean)*(value-new_mean)
        old_mean = new_mean
    return new_mean, variance/count


def get_quantile(data: np.ndarray, prob: float):
    """
    Computes the quantile of a numpy array.

    :param data: The array.
    :param prob: The probability to be under desired quantile.
    :return: The quantile value.
    """
    data = data.flatten()
    data.sort()
    i = int(len(data)*prob + 0.5)
    if i >= len(data):
        return data[-1]
    else:
        return data[i]


def get_workstation_time(size=(1, 5), mean=180, custom=None) -> np.ndarray:
    """
    Get a matrix of random times, in second, where each entry is the time spent
    at a single workstation. To fit the problem we were asked, the matrix
    should be 5 columns wide, because manufactured screens go through 5
    workstations, and have any number of rows (as many as manufactured
    screens).

    The probability distribution of these random time follows an exponential
    distribution.

    :param size: The size of the matrix. The number of row can be seen as the
        number of screens manufactured, and the number of column as the number
        of workstations to go through before completing the screen assembling.
    :param mean: The mean of the exponential distribution.
    :param custom: Use a custom method to compute random numbers (may be
        slower). When set to False or None, uses a numpy function.
        Available custom methods:
          - monte-carlo: Uses a monte-carlo algorithm to compute each number.
          - inversion-sampling: Uses the inverse cumulative function
            of the distribution to sample random numbers.

    :return: A matrix of random times following exponential distribution.
    """
    if not custom:
        return np.random.exponential(mean, size)
    if custom.lower() == 'monte-carlo':
        pass
    elif custom.lower() == 'inversion-sampling':
        return -mean*np.log(1 - np.random.random(size))


def run_simulation(*args):
    """
    Make tests and print report.

    Runnable:
    enter one as argument to run simulation: run('simulation name', ...)

      - inversion-sampling workstation times
      - numpy workstation times
    """
    n = 0
    if 'inversion-sampling workstation times' in args:
        n += 1
        n_trial = int(1e5)
        print('-- Test {}: inversion-sampling workstation times'.format(n))
        for m in 1, 10, 100, 180, 300, 1000:
            try:
                results = get_workstation_time((n_trial, 1), mean=m,
                                               custom='inversion-sampling')
                mean, variance = get_mean_variance(results)
                median = get_quantile(results, 0.5)
                print('   -')
                print('   | number of trials: {}'.format(n_trial))
                print('   | mean    : {: >8d} | {: >11.4e} | error={: >7.5e} '
                      '( {: <2.3%} )'
                      .format(m, mean, abs(m - mean), abs(m-mean)/m))
                print('   | variance: {: >8d} | {: >11.4e} | error={: >7.5e} '
                      '( {: <2.3%} )'
                      .format(m*m, variance, abs(m*m - variance),
                              abs(m*m-variance)/(m*m)))
                print('   | median  : {: >8.3f} | {: >11.4e} | error={: >7.5e} '
                      '( {: <2.3%} )'
                      .format(m*np.log(2), median, abs(m*np.log(2) - median),
                              abs((m*np.log(2)-median)/(m*np.log(2)))))
            except Exception as e:
                print('## Error occurred ##')
                print(repr(e))
        print('   -')
    if 'numpy workstation times' in args:
        n += 1
        n_trial = int(1e5)
        print('-- Test {}: numpy workstation times'.format(n))
        for m in 1, 10, 100, 180, 300, 1000:
            try:
                results = get_workstation_time((n_trial, 1), mean=m)
                mean, variance = get_mean_variance(results)
                median = get_quantile(results, 0.5)
                print('   -')
                print('   | number of trials: {}'.format(n_trial))
                print('   | mean    : {: >8d} | {: >11.4e} | error={: >7.5e} '
                      '( {: <2.3%} )'
                      .format(m, mean, abs(m - mean), abs(m-mean)/m))
                print('   | variance: {: >8d} | {: >11.4e} | error={: >7.5e} '
                      '( {: <2.3%} )'
                      .format(m*m, variance, abs(m*m - variance),
                              abs(m*m-variance)/(m*m)))
                print('   | median  : {: >8.3f} | {: >11.4e} | error={: >7.5e} '
                      '( {: <2.3%} )'
                      .format(m*np.log(2), median, abs(m*np.log(2) - median),
                              abs((m*np.log(2)-median)/(m*np.log(2)))))
            except Exception as e:
                print('## Error occurred ##')
                print(repr(e))
        print('   -')


if __name__ == '__main__':

    if len(sys.argv) > 1:  # If launched with argument from command-line
        run_simulation(sys.argv[1:])
    else:                  # If launched without argument
        run_simulation('inversion-sampling workstation times',
                       'numpy workstation times',
                       )
