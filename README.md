mep_forces.py:

Parses out and plots the evolution of forces and reaction coordinates amongst each intermediate image in a minimum energy pathway (mep) calculation performed with VASP. This is useful for monitoring the evolution of forces relative to convergence criteria during or between job submissions.

Run this script in the home directory, containing the INCAR file and each image sub-directory. By default, the script is executed in the current directory, but other locations can be specified with -i,--input.

The reaction coordinate is normalized so that the image in directory 00/ is at 0.0 and the image in directory images+1/ is at 1.0. The average, minimum, and maximum forces for each intermediate image are compiled for each ionic step and plotted against the number of ionic steps. These are shown alongside the convergence criteria set by EDIFFG, to provide straightforward assessment for the imminence (or lack thereof) of ionic convergence.

Example of intended usage: python mep_forces.py or python mep_forces.py -i my_mep_directory


mep_energy.py:

Plots the energies for each image in a minimum energy pathway (MEP) calculation with VASP. Plotting the initial and final energy profiles is useful for gauging convergence progress during an optimization.

Run this script in the home directory, containing the INCAR file and each image sub-directory. The OUTCARs corresponding to the converged run of the initial and final mep images must be copied into the directories named 00/ and images+1/. By default, the script is executed in the current directory, but other locations can be specified with -i,--input.

The reaction coordinate is normalized so that the image in directory 00/ is at 0.0 and the image in directory images+1/ is at 1.0. Energies are plotted relative to the minimum energy in the MEP series.

Example of intended usage: python mep_energy or python mep_energy -i my_mep_directory


calc_reaction_prefactor.py

Calculates the reaction prefactor from a OUTCAR file for which IBRION=5,6,7,8. Also prints any imagniary energies (in eV) that were excluded from the prefactor product.

mep_trajectory.py

Calculates the displacements of each atom at each image in the mep sequence, relative to their initial positions: ./00/POSCAR. By setting reverse=True as an argument, the final static image is used as the reference for atomic displacements.


Compatible with VASP 5.4.4, Python 2.7.13 and 3.6.5, and VTST 3.2.
