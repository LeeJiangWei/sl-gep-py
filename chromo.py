class Chromosome:
    def __init__(self):
        self.num_data = 0
        self.num_variable = 0
        self.data = [[]]
        pass

    def read_data(self):
        with open("./dataset/F0_0_training_data.txt") as f:
            num_data, num_variable = f.readline().split()
            self.num_data, self.num_variable = int(num_data), int(num_variable)

            data = []
            for line in f:
                row = []
                for c in line.split():
                    row.append(float(c))
                data.append(row)

            self.data = data

    def run(self):
        pass
