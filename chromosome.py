from gene import Gene
import numpy as np
import random
import torch

MAIN_HEAD_LEN = 10
ADF_HEAD_LEN = 3


class Chromosome:
    def __init__(self, var_num=0):
        self.main_program = Gene(MAIN_HEAD_LEN, var_num=var_num, is_adf=False)
        self.adf1 = Gene(ADF_HEAD_LEN, is_adf=True)
        self.adf2 = Gene(ADF_HEAD_LEN, is_adf=True)
        self.main_program.random_init()
        self.adf1.random_init()
        self.adf2.random_init()
        self.gene = self.main_program.gene + self.adf1.gene + self.adf2.gene

        self.fitness = -np.inf

    def eval(self, inputs):
        self.main_program.gene = self.gene[:(2 * MAIN_HEAD_LEN + 1)]
        self.adf1.gene = self.gene[(2 * MAIN_HEAD_LEN + 1):(2 * MAIN_HEAD_LEN + 1) + (2 * ADF_HEAD_LEN + 1)]
        self.adf2.gene = self.gene[(2 * MAIN_HEAD_LEN + 1) + (2 * ADF_HEAD_LEN + 1):(2 * MAIN_HEAD_LEN + 1) + 2 * (
                2 * ADF_HEAD_LEN + 1)]
        self.main_program.compile()
        self.adf1.compile()
        self.adf2.compile()

        def G1(a, b):
            return eval(self.adf1.expression)

        def G2(a, b):
            return eval(self.adf2.expression)

        return eval(self.main_program.expression)

    def compute_fitness(self, data):
        fitness = torch.sqrt(torch.sum((self.eval(data) - data[:, -1]) ** 2) / len(data))

        if torch.isinf(fitness) or torch.isnan(fitness):
            fitness = 100000

        self.fitness = fitness
        return fitness


if __name__ == '__main__':
    GENE_LEN = 34

    NP = 50
    c_rate = 0.05

    population = []

    # random initialization
    for _ in range(NP):
        population.append(Chromosome())

    while True:
        # Mutation
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
