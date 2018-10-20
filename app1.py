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

__author__ = 'Morgan Leclerc'
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
arbitrary large samples, (like the mean, the variances, and quantiles), 
to generate pseudo-random numbers following exponential and gamma 
distributions, and many plot and printing utilities.

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
# from itertools import product
import numpy as np
# import matplotlib.pyplot as plt


def get_mean_variance(data: np.ndarray):
    """
    Computes the mean and the variance of a numpy array using Welford's method.
    Note: The array is flattened before computing.

    :param data: The array.
    :return: A 2-tuple of the mean, variance.
    """
    data = data.flatten()
    # Setup
    old_mean = new_mean = data[0]
    variance = count = 0
    for value in data:
        # At each iteration, update mean and variance
        # This method is greatly documented on internet, and a pseudo-code
        # implementation is presented in a Wikipedia article about computing
        # variance.
        # We use Welford's method to avoid numerical instability when the
        # mean is a lot larger than the standard deviation, or when the size
        # of the sample becomes large.
        count += 1
        new_mean = old_mean + (value-old_mean)/count
        # Variance is the squared distance to the mean
        variance += (value-old_mean)*(value-new_mean)
        old_mean = new_mean
    return new_mean, variance/count  # Don't forget to divide


def get_quantile(data: np.ndarray, prob: float):
    """
    Computes the quantile of a numpy array.

    :param data: The array.
    :param prob: The probability to be under desired quantile.
    :return: The quantile value.
    """
    data = data.flatten()
    # Not the fastest algorithm, but a really simple implementation
    # We first sort the array. So that Wherever we pick a value, every values
    #  before are smaller, and and any other value after are larger.
    data.sort()
    # That means that when we pick the value that is at xx% of the length of
    # the array, xx% of the value are smaller. This is then the quantile of 0.xx
    # Computing the index of the quantile (rounded)
    i = int(len(data)*prob + 0.5)
    if i >= len(data):  # Computation leads to an invalid index if prob ~= 1
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
            Can be ridiculously long !
          - inversion-sampling: Uses the inverse cumulative function
            of the distribution to sample random numbers.

    :return: A matrix of random times following exponential distribution.
    """
    if not custom:
        # Using numpy function
        return np.random.exponential(mean, size)
    if custom.lower() == 'monte-carlo':
        return NotImplemented
    elif custom.lower() == 'inversion-sampling':
        # Following the inverse transform property of cumulative distribution
        # functions, we can generate pseudo random numbers following any
        # distribution from uniformly distributed pseudo-random numbers.
        return -mean*np.log(1 - np.random.random(size))


def run_simulation(*args, n_trials=(1e2, 1e3, 1e4), means=(180,)):
    """
    Run predefined simulations.

    Runnable:
    enter one as argument to run simulation: run('simulation name', ...)

      - inversion-sampling workstation perf: prints performances of
      - numpy workstation perf

    :param args: The simulations to run
    :param n_trials: The size of generated samples. Must be an iterable of
        one or more ints.
    :param means: Means used when generating samples. Must be an iterable of
        one or more ints.
    """
    n = 0  # Number of simulations run
    if 'inversion-sampling workstation perf' in args:
        n += 1
        print('-- Run {}: inversion-sampling workstation performances'
              .format(n))
        for n_trial in n_trials:  # For each number of trials given
            for mean in means:    # For each mean given
                try:
                    # Generate sample
                    results = get_workstation_time((int(n_trial), 1), mean=mean,
                                                   custom='inversion-sampling')
                    # Compute desired quantities
                    s_mean, s_variance = get_mean_variance(results)
                    median = get_quantile(results, 0.5)
                    # Print report
                    # For exponential distributions, standard deviation
                    # equals the mean, and median equals ln(2)*mean
                    print('   -')
                    print('   | number of trials: {:<10.3e}'
                          .format(float(n_trial)))
                    print('   | mean    : {: >8d} | {: >11.4e} | error='
                          '{: >7.5e} ( {: <2.3%} )'
                          .format(mean, s_mean, abs(mean - s_mean),
                                  abs(mean-s_mean)/mean))
                    print('   | std. dev: {: >8d} | {: >11.4e} | error='
                          '{: >7.5e} ( {: <2.3%} )'
                          .format(mean, np.sqrt(s_variance),
                                  abs(mean - np.sqrt(s_variance)),
                                  abs(mean-np.sqrt(s_variance))/mean))
                    print('   | median  : {: >8.3f} | {: >11.4e} | error='
                          '{: >7.5e} ( {: <2.3%} )'
                          .format(mean*np.log(2), median,
                                  abs(mean*np.log(2) - median),
                                  abs((mean*np.log(2)-median)/(mean*np.log(2)))
                                  ))
                except Exception as e:
                    # If an error occurs while running, abort printing and
                    # just print the error
                    print('## Error occurred ##')
                    print(e)
        print('   -')
    if 'numpy workstation perf' in args:
        n += 1
        print('-- Run {}: numpy workstation performances'.format(n))
        for n_trial in n_trials:
            for mean in means:
                try:
                    results = get_workstation_time((int(n_trial), 1), mean=mean)
                    s_mean, s_variance = get_mean_variance(results)
                    median = get_quantile(results, 0.5)
                    print('   -')
                    print('   | number of trials: {:<10.3e}'
                          .format(float(n_trial)))
                    print('   | mean    : {: >8d} | {: >11.4e} | error='
                          '{: >7.5e} ( {: <2.3%} )'
                          .format(mean, s_mean, abs(mean - s_mean),
                                  abs(mean-s_mean)/mean))
                    print('   | variance: {: >8d} | {: >11.4e} | error='
                          '{: >7.5e} ( {: <2.3%} )'
                          .format(mean*mean, s_variance,
                                  abs(mean*mean - s_variance),
                                  abs(mean*mean-s_variance)/(mean*mean)))
                    print('   | median  : {: >8.3f} | {: >11.4e} | error='
                          '{: >7.5e} ( {: <2.3%} )'
                          .format(mean*np.log(2), median,
                                  abs(mean*np.log(2) - median),
                                  abs((mean*np.log(2)-median)/(mean*np.log(2)))
                                  ))
                except Exception as e:
                    print('## Error occurred ##')
                    print(repr(e))
        print('   -')


if __name__ == '__main__':

    if len(sys.argv) > 1:  # If launched with argument from command-line
        run_simulation(sys.argv[1:])
    else:                  # If launched without argument
        run_simulation('inversion-sampling workstation perf',
                       'numpy workstation perf',
                       )
