def read_data(path="./dataset/F0_0_training_data.txt"):
    with open(path) as f:
        num_data, num_variable = f.readline().split()
        num_data, num_variable = int(num_data), int(num_variable)
        data = []
        for line in f:
            row = []
            for c in line.split():
                row.append(float(c))
            data.append(row)
        return num_data, num_variable, data


if __name__ == '__main__':
    print(read_data())
