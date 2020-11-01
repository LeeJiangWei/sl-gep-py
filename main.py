import random
import re
import torch

from gene import FUNCTION, ADF, TERMINAL, INPUT_ARGUMENT
from chromosome import Chromosome, MAIN_HEAD_LEN, ADF_HEAD_LEN
from read_data import read_data
from roulette_wheel import roulette_wheel

GENE_LEN = 2 * MAIN_HEAD_LEN + 1 + 2 * (2 * ADF_HEAD_LEN + 1)
NP = 50
c_rate = 0.05

MAIN_START = 0
MAIN_END = MAIN_START + 2 * MAIN_HEAD_LEN + 1
ADF1_START = MAIN_END
ADF1_END = ADF1_START + 2 * ADF_HEAD_LEN + 1
ADF2_START = ADF1_END
ADF2_END = ADF2_START + 2 * ADF_HEAD_LEN + 1

FUNCTION_ADF = FUNCTION + ADF

# read data
nd, nv, data = read_data()  # "./dataset/F49_2_training_data.txt"
cuda = torch.device("cuda")
data = torch.tensor(data)

population = []

for _ in range(NP):
    # random initialization
    c = Chromosome(var_num=nv)

    # evaluate initial population
    c.compute_fitness(data)

    population.append(c)

for epo in range(1000000):
    # population.sort(key=lambda x: x.fitness)
    # best_individual = population[0]
    best_individual = sorted(population, key=lambda x: x.fitness)[0]

    if epo % 10 == 0:
        print("epoch:", epo, " fitness:", best_individual.fitness)
        print(best_individual.gene)

        if best_individual.fitness < 1e-5:
            break

    # compute symbol frequency in main program
    function_adf_count_list = [0] * len(FUNCTION_ADF)
    terminal_count_list = [0] * (len(TERMINAL) + nv)
    function_adf_count = 0

    # update frequency
    for c in population:
        for ind in range(MAIN_HEAD_LEN):
            value = c.gene[ind]
            if value in FUNCTION_ADF:
                function_adf_count_list[FUNCTION_ADF.index(value)] += 1
                function_adf_count += 1
            elif value in TERMINAL:
                terminal_count_list[TERMINAL.index(value)] += 1
            else:
                terminal_count_list[int(re.findall(r"\d+", value)[0]) + len(TERMINAL)] += 1

    theta = function_adf_count / (NP * MAIN_HEAD_LEN)

    i = 0
    while i < NP:
        F = random.random()
        CR = random.random()

        # pick 2 random distinct indexes of chromosome
        r1 = r2 = i
        while r1 == i:
            r1 = random.randint(0, NP - 1)
        while r2 == i or r2 == r1:
            r2 = random.randint(0, NP - 1)
        k = random.randint(0, GENE_LEN - 1)

        # trial vector
        u = Chromosome(var_num=nv)

        for j in range(GENE_LEN):
            # compute mutate probability
            phi = 1 - (1 - F * int(best_individual.gene[j] != population[i].gene[j])) \
                  * (1 - F * int(population[r1].gene[j] != population[r2].gene[j]))

            # mutate & crossover
            if (random.random() < CR or j == k) and random.random() < phi:
                # frequency-based assignment
                new_symbol = ""
                # main head
                if MAIN_START <= j < MAIN_END - MAIN_HEAD_LEN - 1:
                    if random.random() < theta:
                        index = roulette_wheel(function_adf_count_list)
                        new_symbol = FUNCTION_ADF[index]
                    else:
                        index = roulette_wheel(terminal_count_list)
                        if index < len(TERMINAL):
                            new_symbol = TERMINAL[index]
                        else:
                            new_symbol = f"inputs[:, {index - len(TERMINAL)}]"
                # main tail
                elif MAIN_START + MAIN_HEAD_LEN <= j < MAIN_END:
                    index = roulette_wheel(terminal_count_list)
                    if index < len(TERMINAL):
                        new_symbol = TERMINAL[index]
                    else:
                        new_symbol = f"inputs[:, {index - len(TERMINAL)}]"
                # adf head
                elif ADF1_START <= j < ADF1_END - ADF_HEAD_LEN - 1 or \
                        ADF2_START <= j < ADF2_END - ADF_HEAD_LEN - 1:
                    flag = random.randint(0, 1)
                    if flag:
                        index = random.randint(0, len(FUNCTION) - 1)
                        new_symbol = FUNCTION[index]
                    else:
                        index = random.randint(0, len(INPUT_ARGUMENT) - 1)
                        new_symbol = INPUT_ARGUMENT[index]
                # adf tail
                elif ADF1_START + ADF_HEAD_LEN <= j < ADF1_END or \
                        ADF2_START + ADF_HEAD_LEN <= j < ADF2_END:
                    index = random.randint(0, len(INPUT_ARGUMENT) - 1)
                    new_symbol = INPUT_ARGUMENT[index]

                u.gene[j] = new_symbol
            else:
                u.gene[j] = population[i].gene[j]

        # selection
        u.compute_fitness(data)
        if u.fitness <= population[i].fitness:
            population[i] = u

        i += 1

best_individual = sorted(population, key=lambda x: x.fitness)[0]
print(best_individual.gene)
print(best_individual.fitness)
