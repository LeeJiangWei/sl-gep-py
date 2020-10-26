import random

from chromosome import Chromosome
from read_data import read_data

GENE_LEN = 34
NP = 50
c_rate = 0.05

population = []

# random initialization
for _ in range(NP):
    population.append(Chromosome())

# evaluate initial population
data_set = read_data()

for ind in population:
    sum_of_square = 0
    for data in data_set:
        o = ind.eval(x=data[0])
        y = data[1]
        square = (y - o) ** 2


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
