import random

def roulette_wheel(count_list):
    sum = 0
    for i in count_list:
        sum += i + 1

    normalized_list = count_list.copy()
    for i in range(len(normalized_list)):
        normalized_list[i] = (normalized_list[i]+1)/sum

    sorted_list = sorted(enumerate(normalized_list), key=lambda x:x[1])
    
    p = random.random()
    i = -1
    while p > 0:
        i += 1
        p -= sorted_list[i][1]

    return sorted_list[i][0]


if __name__ == "__main__":
    count = [22,3,34,6,67,0]
    c = [0] * len(count)
    for _ in range(1000):
        i = roulette_wheel(count)
        c[i] += 1
    
    print(c)
