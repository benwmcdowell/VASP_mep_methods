# mep_forces_from_VASP
Parses out and plots the evolution of forces and reaction coordinates amongst each intermediate image in a minimum energy pathway (mep) calculation performed with VASP. This is useful for monitoring the evolution of forces relative to convergence criteria during or between job submissions.

Run this script in the home directory, containing the INCAR file and each image sub-directory. The OUTCARs corresponding to the converged run of the initial and final mep images must be copied into the directories named 00/ and images+1/. By default, the script is executed in the current directory, but other locations can be specified with -i,--input.

The reaction coordinate is normalized so that the image in directory 00/ is at 0.0 and the image in directory images+1/ is at 1.0. The average, minimum, and maximum forces for each intermediate image are compiled for each ionic step and plotted against the number of ionic steps. These are shown alongside the convergence criteria set by EDIFFG, to provide straightforward assessment for the imminence (or lack thereof) of ionic convergence.

Example of intended usage: python mep_forces.py or python mep_forces.py -i my_mep_directory

Compatible with VASP 5.4.4, Python 2.7.13 and 3.6.5, and VTST 3.2.
