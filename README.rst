AMSIMP Initial Atmospheric Conditions Data Repository
=====================================================

|GitHub last commit| |Data Build|

This is the data repository for the initial atmospheric conditions
utilised within AMSIMP. The data is acquired from the NRLMSISE-00
Atmospheric Model, using a Python API known as `msise00`_ as an
interface to the Fortran code. NRLMSISE-00 is an empirical, global
reference atmospheric model of the Earth from ground to space. It models
the temperatures and densities of the atmosphere’s components. Using the
Ideal Gas Law, the atmospheric pressure is calculated using the
temperature and atmospheric density. These three key atmospheric
parameters will then be utilised to determine the geostrophic wind, the
pressure thckness, etc. For more information on the mathematics used
within AMSIMP, read the `documentation <https://docs.amsimp.com/math.html>`_
for a brief outline, or read the `paper <https://github.com/amsimp/papers/raw/master/project-book/main.pdf>`_
for a detailed report on the software.

Future Plans
------------

The software is currently in a beta release state. It must be noted that the
data provided by the NRLMSISE-00 Atmospheric Model has a mean absolute
percentage error of approximately 1.5% and a median absolute percentage error
of approximately 0.8% in relation to actual atmospheric conditions. While one
might argue that this is reasonable accurate, as a consequence of Chaos Theory,
a tiny difference in the initial conditions in a large system can result in
drastically different forecasted events. The atmosphere is such a system, and
such a system is known as a chaotic dynamical system. Therefore, for the
release candidate version of the software, a switch to live (close to it)
atmospheric data will be made in order to enhance the accuracy of the software.
The release candidate version of the software is planned for release in
Fall 2020.

.. _msise00: https://pypi.org/project/msise00/

.. |GitHub last commit| image:: https://img.shields.io/github/last-commit/amsimp/amsimp?label=Last%20Data%20Update
.. |Data Build| image:: https://github.com/amsimp/amsimp-data/workflows/Hourly%20Update%20of%20Data/badge.svg
