#!/usr/bin/python4

"""
Error calculation functions.

"""

from collections import Counter

def avg(samples):
	"""
	Average of the given samples

	.. math::

		a = \frac{1}{N} \sum\limits^{N}_{i = 1} x_i
	"""
	return sum(samples)/len(samples)

def modus(samples):
	"""
	Modus of the given samples (most common)
	"""
	return Counter(samples).most_common()[0][0]


def average_absolute_error(samples):
	"""
	The average absolute error of the given samples.

	.. math::

		\Delta x = \frac{1}{N} \sum\limits^{N}_{i = 1} | x_i - a |
	"""
	a = avg(samples)
	return sum([abs(x - a) for x in samples])/len(samples)

def relative_error(samples):
	"""
	Relative Error of the given samples

	.. math::

		\gamma = \frac{\Delta x}{a}
	"""
	return abs(average_absolute_error(samples) / avg(samples))


