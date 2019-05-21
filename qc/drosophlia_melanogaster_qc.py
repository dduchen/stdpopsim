import msprime
import numpy as np
import math
import stdpopsim.models as models

class LiStephanTwoPopulation(models.Model):
    def __init__(self):
        super().__init__()
        # Parameters for the African population are taken from the section Demographic
        # History of the African Population
        generation_time = 0.1 ## 10  generations per year
        N_A0 = 8.603e6 # modern African pop. size
        N_A1 = N_A0/5.0 # African pop. size before expansion

        # Parameters for the European population are taken from the section Demographic
        # History of the European Population
        N_E0 = 1.075e6 # modern European pop. size
        N_E1 = 2.2e3 # European founder pop. size

        # Times from from the section Demographic History of the * Population
        T_A0 = 6e4/generation_time # time of 1st expansion in African pop.
        T_E_A = 15.8e3/generation_time # European/African divergence time
        T_EE = T_E_A - 340/generation_time # Time of European pop. re-expansion 

        # Set population sizes at T=0
        # pop0 is Africa, pop1 is Europe
        self.population_configurations = [
            msprime.PopulationConfiguration(
                initial_size=N_A0, growth_rate=0),
            msprime.PopulationConfiguration(
                initial_size=N_E0, growth_rate=0),
        ]

        # Migration matrix, all migrations to admixed population are 0
        self.migration_matrix = [
            [0, 0],
            [0, 0]
        ]

        # Now we add the demographic events working backwards in time. 
        self.demographic_events = [
            ## OOA bottleneck
            msprime.PopulationParametersChange(
                time=T_EE, initial_size=N_E1, population_id=1),
            # E and A coalesce
            msprime.MassMigration(
                time=T_E_A, source=1, destination=0, proportion= 1.0),
            ## Pre-expansion Africa
            msprime.PopulationParametersChange(
                time=T_A0, initial_size=N_A1, population_id=0),
        ]
