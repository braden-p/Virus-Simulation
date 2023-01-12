"""
Virus Simulation
Created by Braden Piper, bradenpiper.com
Created on Wed Jan 11, 2023
Version = 1.1
------------------------------------------
DESCRIPTION:
A stochastic simulation of a virus population within a human body. In this
simulation, in a given time step, a SimpleVirus has a probability of
reproducing and a probability of dying and being cleared from the patient.
A ResistantVirus inherits from SimpleVirus, and also has a probablity that
its offspring will develop a resistance to any drugs.
There is a maximum limit to the size of the virus population within the body,
and as the population density increases, the likelihood that a virus will
reproduce decreases.
A TreatedPatient inherits from Patient, and can be prescribed medication.
If a virus is not resistant to a medication that has been taken by the
TreatedPatient, it will not reproduce.
The simulationWithDrug and simulationWithoutDrug functions allow the user
to run the virus simulation for 300 time steps and with their desired parameters
over multiple trials, and will plot the average results of the trials. In the
simulationWithDrug function, a drug is administered at the 150th time step.
The customizable parameters for these simulations are:
    - The number of viruses to start with (numViruses)
    - The maximum virus population (maxPop)
    - The probability the virus will reproduce (maxBirthProb)
    - The probability the virus will die (clearProb)
    - Which drugs the virus population has resistance to at the start (resistances)
    - The probablity the virus offspring will gain or lose resistance to a drug (mutProb)
    - The number of trials to run (numTrials)
Scroll to the bottom of this program to uncomment the simulation lines of code,
and run the program.
------------------------------------------
NOTE: This program was completed as part of the course MITx 6.00.2x - Introduction
to Computational Thinking and Data Science. The general framework, and some
of the functions were provided materials. The majority of the implementation is
my own work.
The following class was provided:
    NoChildException
All of the remaining class and function names were provided with docstrings,
but the implementations are my own work
"""

import random
import pylab


class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def __str__(self):
        return 'Simple Virus with maxBirthProb:'+str(self.maxBirthProb)+' and clearProb:'+str(self.clearProb)

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        return random.random() < self.getClearProb()
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        if random.random() < self.maxBirthProb*(1-popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def __str__(self):
        return 'Patient with'+str(self.getTotalPop())+' viruses and maxPop:'+str(self.maxPop)

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.getViruses())        


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        for virus in self.getViruses():
            if virus.doesClear():
                self.viruses.remove(virus)
        popDensity = len(self.getViruses()) / self.getMaxPop()
        for virus in self.getViruses():
            try:
                self.viruses.append(virus.reproduce(popDensity))
            except NoChildException:
                pass
        return len(self.getViruses())


def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """   
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    trialCounter = 0
    virusPop = []
    for trial in range(numTrials):
        trialCounter += 1
        viruses = []
        for num in range(numViruses):
            viruses.append(SimpleVirus(maxBirthProb, clearProb))
        patient = Patient(viruses, maxPop)

        timesteps = []
        counter = 0
        if trialCounter == 1:
            for timestep in range(300):
                counter += 1
                timesteps.append(counter)
                patient.update()
                virusPop.append(patient.getTotalPop())
        else:
            for timestep in range(300):
                counter += 1
                timesteps.append(counter)
                patient.update()
                virusPop[counter-1] += patient.getTotalPop()
    virusPopAvg = []
    for item in virusPop:
        virusPopAvg.append(item/numTrials)
  
    pylab.plot(virusPopAvg, label = 'SimpleVirus')    
    pylab.title('SimpleVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.legend(loc = 'best')
    pylab.show()


class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb
        
    def __str__(self):
        return 'Resistant Virus with maxBirthProb:'+str(self.maxBirthProb)+' , clearProb:'+str(self.clearProb)+' ,resistances:'+str(self.getResistances())+' ,mutProb:'+str(self.mutProb)
        

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.getMutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        return self.getResistances().get(drug)


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        for drug in activeDrugs:  # check if virus resistant to all activeDrugs
            if self.isResistantTo(drug):
                continue
            else:
                raise NoChildException 
        if random.random() < self.maxBirthProb * (1 - popDensity):
            resistanceKeys = self.getResistances().keys()
            resistanceValues = self.getResistances().values()
            for drug in resistanceKeys:
                if random.random() < 1-self.mutProb:
                    if self.resistances[drug] == True:    
                        self.resistances[drug] = True
                    else:
                        self.resistances[drug] = False
                else:
                    if self.resistances[drug] == False:
                        self.resistances[drug] = True
                    else:
                        self.resistances[drug] = False
        else:
            raise NoChildException
        
        return ResistantVirus(self.maxBirthProb, self.clearProb, self.resistances, self.mutProb)
            

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        self.viruses = viruses
        self.maxPop = maxPop
        self.drugs = []

    def __str__(self):
        return 'TreatedPatient with'+str(self.getTotalPop())+' viruses and maxPop:'+str(self.maxPop)
    

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.drugs
        


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        resistantPop = 0
        for virus in self.viruses:
            numDrugsResistant = 0
            for drug in drugResist:
                if virus.isResistantTo(drug):
                    numDrugsResistant += 1
            if numDrugsResistant == len(drugResist):
                resistantPop += 1
        return resistantPop


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() executes these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        activeDrugs = self.getPrescriptions()
        children = []
        for virus in self.getViruses():
            if virus.doesClear():
                self.viruses.remove(virus)
        popDensity = len(self.getViruses()) / self.getMaxPop()
        for virus in self.getViruses():
            try:
                children.append(virus.reproduce(popDensity,activeDrugs))
            except NoChildException:
                pass
        for child in children:
            self.viruses.append(child)
        return len(self.getViruses())


def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                        mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                  (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
              (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """

    trialCounter = 0
    virusPop = []
    resistantVirusPop = []
    for trial in range(numTrials):
        trialCounter += 1
        viruses = []
        for num in range(numViruses):
            viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
        patient = TreatedPatient(viruses, maxPop)

        timesteps = []
        counter = 0
        if trialCounter == 1:               # first trial sets 150 slots for virusPop
            for timestep in range(150):
                counter += 1
                timesteps.append(counter)   # keep track of # of timesteps
                patient.update()            # update 150 times
                virusPop.append(patient.getTotalPop())   # add total virus populations to virusPop
                resistantVirusPop.append(patient.getResistPop(['guttagonol']))
            patient.addPrescription('guttagonol')   #  add guttagonol drug
            for timestep in range(150):
                counter += 1
                timesteps.append(counter)   # keep track of # of timesteps
                patient.update()            # update 150 times
                virusPop.append(patient.getTotalPop())   # add total virus populations to virusPop
                resistantVirusPop.append(patient.getResistPop(['guttagonol']))
        
        else:
            for timestep in range(150):    # subsequent trials add virusPop to corresponding index
                counter += 1
                timesteps.append(counter)
                patient.update()
                virusPop[counter-1] += patient.getTotalPop()
                resistantVirusPop[counter-1] += patient.getResistPop(['guttagonol'])
            patient.addPrescription('guttagonol')
            for timestep in range(150):    
                counter += 1
                timesteps.append(counter)
                patient.update()
                virusPop[counter-1] += patient.getTotalPop()
                resistantVirusPop[counter-1] += patient.getResistPop(['guttagonol'])
    virusPopAvg = []
    resistantVirusPopAvg = []
    print('Total Virus Pop:', virusPop)
    print('Resistant Virus Pop:', resistantVirusPop)
    for item in virusPop:
        virusPopAvg.append(item/numTrials)
    for item in resistantVirusPop:
        resistantVirusPopAvg.append(item/numTrials)
    print('Avg Total Virus Pop:', virusPopAvg)
    print('Avg Resistant Virus Pop:', resistantVirusPopAvg)
  
    pylab.plot(virusPopAvg, label = 'Total')
    pylab.plot(resistantVirusPopAvg, label = 'ResistantVirus')    
    pylab.title('ResistantVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.legend(loc = 'best')
    pylab.show()


# SIMULATION WITHOUT DRUG
# Uncomment this line to run the simulation without drug
# These are the simulationWithoutDrug parameters:
# (numViruses, maxPop, maxBirthProb, clearProb, numTrials)
##simulationWithoutDrug(100, 1000, 0.1, .05, 100)

# SIMULATION WITH DRUG
# Uncomment this line to run the simulation with drug
# These are the simulationWithDrug parameters:
# (numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numTrials)
##simulationWithDrug(100, 1000, 0.1, .05, {'guttagonol': False}, .005, 100)