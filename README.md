# Virus Simulation
#### Created by Braden Piper, bradenpiper.com
#### Created on Wed Jan 11, 2023
#### Version = 1.1
---
## DESCRIPTION
A stochastic simulation of a virus population within a `Patient`. In this
simulation, in a given time step, a `SimpleVirus` has a probability of
reproducing and a probability of dying and being cleared from the patient.
A `ResistantVirus` inherits from `SimpleVirus`, and also has a probablity that
its offspring will develop a resistance to any drugs.
There is a maximum limit to the size of the virus population within the body,
and as the population density increases, the likelihood that a virus will
reproduce decreases.

A `TreatedPatient` inherits from `Patient`, and can be prescribed medication.
If a virus is not resistant to a medication that has been taken by the
TreatedPatient, it will not reproduce.

The `simulationWithDrug` and `simulationWithoutDrug` functions allow the user
to run the virus simulation for 300 time steps and with their desired parameters
over multiple trials, and will plot the average results of the trials. In the
`simulationWithDrug` function, the drug guttaginol is administered at the 150th time step.
The customizable parameters for these simulations are:
* The number of viruses to start with (numViruses)
* The maximum virus population (maxPop)
* The probability the virus will reproduce (maxBirthProb)
* The probability the virus will die (clearProb)
* Which drugs the virus population has resistance to at the start (resistances)
* The probablity the virus offspring will gain or lose resistance to a drug (mutProb)
* The number of trials to run (numTrials)

Scroll to the bottom of this program to uncomment the simulation lines of code, and run the program.

---
## INSTRUCTIONS
* Open virus_simulation.py
* Scroll to the bottom, and uncomment specific lines of code depending on what you want to do
---
##### NOTE:
NOTE: This program was completed as part of the course MITx 6.00.2x - Introduction
to Computational Thinking and Data Science. The general framework, and some
of the functions were provided materials. The majority of the implementation is
my own work.
The following class was provided:
* `NoChildException`

All of the remaining class and function names were provided with docstrings,
but the implementations are my own work