#!/usr/bin/python3
"""
Copyright © Morgan Leclerc (2018)

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
__version__ = '1.0'
__doc__ = '''
This module is governed by the CeCILL-B license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL-B
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

This module provides parsing functions to handle nicely sometimes intricate 
data structures layout. 

This module needs Python 3.5+ to run
'''

# Major revision, Minor revision, Stability (True=stable)
VERSION_INFO = (1, 0, True)


def parse_summary(reports: list, prints: bool=True, titles: list=None) -> str:
    """
    Convert summary to strings nicely.

    :param reports: The report to print as a list of dict.
    :param prints: True to print parsed string.
    :param titles: The titles of each column of the reports summary, in order.
        If a report field is not in the given titles, it is appended to the
        reports summary titles.
    """
    if titles is None:
        titles = []

    for reprt in reports:
        for title in reprt:
            if title not in titles:
                titles.append(title)

    lengths = {title: len(title) for title in titles}
    for title in titles:
        for reprt in reports:
            if title in reprt and len(str(reprt[title])) > lengths[title]:
                lengths[title] = len(str(reprt[title]))

    lines = '|' + '|'.join([' ' + title + ' '*(lengths[title]-len(title))
                           for title in titles]) + '|\n'
    lines += '|' + '|'.join([':' + '-'*(lengths[title]-1) + ':'
                            for title in titles]) + '|\n'

    for reprt in reports:
        lines += '|'
        for title in titles:
            lines += ' '
            lines += str(reprt[title])
            lines += ' '*(lengths[title]-len(str(reprt[title])))
            lines += '|'
        lines += '\n'

    if prints:
        print(lines)
