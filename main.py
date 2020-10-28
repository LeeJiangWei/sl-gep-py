import random

from gene import FUNCTION_A1, FUNCTION_A2, ADF
from chromosome import Chromosome, MAIN_HEAD_LEN, ADF_HEAD_LEN
from read_data import read_data

GENE_LEN = 2*MAIN_HEAD_LEN+1 + 2*(2*ADF_HEAD_LEN+1)
NP = 50
c_rate = 0.05

MAIN_START = 0
MAIN_END = MAIN_START + 2*MAIN_HEAD_LEN+1
ADF1_START = MAIN_END
ADF1_END = ADF1_START + 2*ADF_HEAD_LEN+1
ADF2_START = ADF1_END
ADF2_END = ADF2_START + 2*ADF_HEAD_LEN+1

# read data
nd, nv, data = read_data("./dataset/F49_2_training_data.txt")

population = []

for _ in range(NP):
    # random initialization
    c = Chromosome(var_num=nv)

    # evaluate initial population
    c.compute_fitness(data)

    population.append(c)

while True:
    # population.sort(key=lambda x: x.fitness)
    # best_individual = population[0]
    best_individual = sorted(population, key=lambda x: x.fitness)[0]

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

        # trail vector
        u = Chromosome(var_num=nv)

        # compute symbol frequency in main program
        head_frequency = {}
        head_sum = NP * MAIN_HEAD_LEN
        tail_frequency = {}
        tail_sum = NP * (MAIN_HEAD_LEN + 1)
        func_num = 0

        for c in population:
            for index, value in enumerate(c.gene):
                if index < MAIN_HEAD_LEN:
                    if value not in head_frequency.keys():
                        head_frequency[value] = 0
                    head_frequency[value] += 1

                    if value in FUNCTION_A1+FUNCTION_A2+ADF:
                        func_num += 1
                else:
                    if value not in tail_frequency.keys():
                        tail_frequency[value] = 0
                    tail_frequency[value] += 1

        head_frequency = sorted(head_frequency.items(), key=lambda x: x[1])
        tail_frequency = sorted(tail_frequency.items(), key=lambda x: x[1])
        theta = func_num / head_sum # proportion of func and adf in head

        for j in range(GENE_LEN):
            # compute mutate probability
            phi = 1 - (1 - F * int(best_individual.gene[j] != population[i].gene[j])) \
                * (1 - F * int(population[r1].gene[j] != population[r2].gene[j]))

            # mutate & crossover
            if (random.random() < CR or j==k) and random.random() < phi:
                # frequency-based assignment
                u.gene[j] = 1
                # main head
                if MAIN_START <= j < MAIN_END-MAIN_HEAD_LEN-1:
                    pass
                # main tail
                elif MAIN_START + MAIN_HEAD_LEN <= j < MAIN_END:
                    pass
                # adf head
                elif ADF1_START <= j < ADF1_END-ADF_HEAD_LEN-1 or \
                    ADF2_START <= j < ADF2_END-ADF_HEAD_LEN-1:
                    pass
                # adf tail
                elif ADF1_START + ADF_HEAD_LEN <= j < ADF1_END or \
                    ADF2_START + ADF_HEAD_LEN <= j < ADF2_END:
                    pass
            else:
                u.gene[j] = population[i][j]
        break

        # selection

    break
