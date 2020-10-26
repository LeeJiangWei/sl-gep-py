def read_data(path="./dataset/F0_0_training_data.txt"):
    with open(path) as f:
        num_data, num_variable = f.readline().split()
        data = []
        for line in f:
            row = []
            for c in line.split():
                row.append(float(c))
            data.append(row)
        return data


if __name__ == '__main__':
    print(read_data())
