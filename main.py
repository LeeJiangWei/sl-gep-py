import random

from chromosome import Chromosome, MAIN_HEAD_LEN, ADF_HEAD_LEN
from read_data import read_data

GENE_LEN = 2*MAIN_HEAD_LEN+1 + 2*(2*ADF_HEAD_LEN+1)
NP = 50
c_rate = 0.05

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

    # mutation
    i = 0
    while i < NP:
        F = random.random()
        print("F: ", F)
        CR = random.random()

        r1 = r2 = i
        while r1 == i:
            r1 = random.randint(0, NP - 1)
        while r2 == i or r2 == r1:
            r2 = random.randint(0, NP - 1)
        
        k = random.randint(0, GENE_LEN - 1)
        for j in range(GENE_LEN):
            # print("best j: ", best_individual.gene[j])
            # print("i j: ", population[i].gene[j])
            # print("r1 j: ", population[r1].gene[j])
            # print("r2 j: ", population[r2].gene[j])

            phi = 1 - (1 - F * int(best_individual.gene[j] != population[i].gene[j])) \
                * (1 - F * int(population[r1].gene[j] != population[r2].gene[j]))
            print(phi)

            if (random.random() < CR or j==k) and random.random() < phi:
                u = fs()
            else:
                u = x
        break
    break
