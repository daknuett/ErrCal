ErrCal -- Online Error Calculation
**********************************

.. contents::

Getting Started
===============

The first step towards error calculation is to collect the
data. Usually the values will be measured by hand, so one
will go to `/index.html` and add a new row.

A row represents one series of measurements, for instance if
one has to measure the commute of a pendulum, he will do so
about 5-10 times for every parameter. So you have to enter
the number of measurements in the box before the "Add Row"
button. Then click on "Add Row".

If you have finished one series of measurements, click on
"Add Row" again.

If all the samples are inserted the errors can be calculated
by clicking on "Calculate". The button "Download" will open
a new tab with the calculated results.

Data Formats
============

The download function supports currently three formats:
``csv``, ``json`` and ``ljson``. These should fit all
purposes. 

Calculation
===========

The calculation is based on the following formulas:


.. math::

	a = \frac{1}{N} \sum\limits^{N}_{i = 1} x_i

.. math::

	\Delta x = \frac{1}{N} \sum\limits^{N}_{i = 1} | x_i - a |

.. math::

	\gamma = \frac{\Delta x}{a}

Modus:

	>>> Counter(samples).most_common()[0][0]

