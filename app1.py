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


import numpy as np
import matplotlib.pyplot as plt


def get_workstation_time(size=(1,5), mean=180, manual=True) -> float:
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
    :param manual: Set to true to compute exponential distribution from
        equiprobable random numbers (slower). When set to false, uses the
        numpy function.

    :return: A matrix of random times following exponential distribution.
    """