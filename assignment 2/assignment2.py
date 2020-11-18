# Them cac thu vien neu can
import numpy as np
from itertools import combinations, permutations

def readinput(filename):
    with open(filename, 'r') as fi:
        rawgarage = [int(i) for i in fi.readline().split()]
        numworkers, numpackets = [int(i) for i in fi.readline().split()]
        rawpackets = []
        for _ in range(numpackets):
            rawpackets.append([int(i) for i in fi.readline().split()])

        garage = np.array(rawgarage)
    return garage, numworkers, numpackets, rawpackets

def preprocessing(rawpackets):
    packets = np.array([np.array([i, j, 5 + k + l * 2]) for i, j, k, l in rawpackets])
    return packets

def f(packets, garage):
    if len(packets) == 0:
        return 0
    income = sum(packets[:,2])

    len2 = lambda x, y: np.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)
    move = np.concatenate([np.array([garage]), packets[:, :2]])

    length = sum([len2(move[i], move[i + 1]) for i in range(len(packets))])
    outcome = length * 10 / 20 + 10
    return income - outcome

def minfunction(garage, workerassignment, packets):
    summing = np.array([])
    for i in workerassignment:
        summing = np.append(summing, np.array(f(np.array([packets[j] for j in i]), garage)))

    minf = 0
    print(summing)
    for i, j in combinations(summing, 2):
            minf += abs(i - j)
    return minf

def assign(file_input, file_output):
    # read input
    garage, numworkers, numpackets, rawpackets = readinput("input.txt")
    packets = preprocessing(rawpackets)
    print(packets)
    
    for i in permutations()
    wass = [[1],
            []]
    # for i in range(numworkers * numpackets):
    #     a = [[], []]
    #     for j in range(numpackets):
    #         for k in range(numworkers):
    #             a[k].append(j)

    #     wass.append(a) 

    m = minfunction(garage, wass, packets)
    print(m)

    # m = minfunction(garage, workerassignment, packets)
    # print(m)
    # run algorithm



    # write output
    return


assign('input.txt', 'output.txt')
