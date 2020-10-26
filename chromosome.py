from gene import Gene
import numpy as np
import random

FUNCTION_A1 = ["np.sin({})", "np.cos({})", "np.exp({})", "np.log(np.abs({}))"]
FUNCTION_A2_MAIN = ["({} + {})", "({} - {})", "({} * {})", "({} / {})", "G1({}, {})", "G2({}, {})"]
FUNCTION_A2_ADF = ["({} + {})", "({} - {})", "({} * {})", "({} / {})"]

TERMINAL_MAIN = ["np.pi", "x"]
TERMINAL_ADF = ["a", "b"]


class Chromosome:
    def __init__(self):
        self.main_program = Gene(10, FUNCTION_A1, FUNCTION_A2_MAIN, TERMINAL_MAIN)
        self.adf1 = Gene(3, FUNCTION_A1, FUNCTION_A2_ADF, TERMINAL_ADF)
        self.adf2 = Gene(3, FUNCTION_A1, FUNCTION_A2_ADF, TERMINAL_ADF)
        self.main_program.random_init()
        self.adf1.random_init()
        self.adf2.random_init()
        self.gene = self.main_program.gene + self.adf1.gene + self.adf2.gene

        self.fitness = -np.inf

    def eval(self, x=1, y=1, z=1):
        self.main_program.compile()
        self.adf1.compile()
        self.adf2.compile()

        def G1(a, b):
            return eval(self.adf1.expression)

        def G2(a, b):
            return eval(self.adf2.expression)

        try:
            fitness = eval(self.main_program.expression)
            if np.isnan(fitness):
                self.fitness = np.inf
            elif np.isinf(fitness):
                self.fitness = np.inf
            else:
                self.fitness = fitness
            return self.fitness
        except ZeroDivisionError:
            print("Warning: Divided by 0.")
            self.fitness = np.inf
            return self.fitness


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
