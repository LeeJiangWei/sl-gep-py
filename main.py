import random

from chromosome import Chromosome
from read_data import read_data

GENE_LEN = 34
NP = 50
c_rate = 0.05

# read data
nd, nv, data_set = read_data()

population = []

for _ in range(NP):
    # random initialization
    c = Chromosome(var_num=nv)

    # evaluate initial population
    c.compute_fitness()

    population.append(c)

while True:
    # mutation
    i = 0
    while i < NP:
        F = random.random()
        CR = random.random()

        r1 = r2 = i
        while r1 == i:
            r1 = random.randint(0, NP - 1)
        while r2 == i or r2 == r1:
            r2 = random.randint(0, NP - 1)

        k = random.randint(0, GENE_LEN - 1)
        for j in range(GENE_LEN):
            pass
