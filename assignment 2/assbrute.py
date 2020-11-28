# Them cac thu vien neu can
import math
import random
from itertools import combinations
import time


# OBJECT
class Pack():
    def __init__(self, i, j, k, l, idx = -1):
        self.x = int(i)
        self.y = int(j)
        self.earn = int(k) + int(l) * 2 + 5    #ATTENTION
        self.idx = idx

    def __sub__(self, obj):
        return math.sqrt((self.x - obj.x)**2 + (self.y - obj.y)**2)

    def __str__(self):
        return "#" + str(self.idx) #+ " loc: " + str(self.x) + ", " \
            #+ str(self.y) + ", income: " + str(self.earn)


# READ UTILITIES
def readinput(filename):
    with open(filename, 'r') as fi:
        # create garage
        rawgarage = [int(i) for i in fi.readline().split()]
        # garage = Pack(rawgarage[0], rawgarage[1], -5, 0)
        garage = Pack(rawgarage[0], rawgarage[1], -5, 0)  #ATTENTION

        # num
        numworkers, numpackets = [int(i) for i in fi.readline().split()]

        # packets
        packets = []
        for i in range(numpackets):
            r = fi.readline().split()
            packets.append(Pack(r[0], r[1], r[2], r[3], i))

    return garage, numworkers, numpackets, packets

# WRITE UTILITIES
def writeoutput(filename, worker):
    with open(filename, 'w') as fo:
        for packs in worker:
            for i in packs[:-1]:
                fo.write("%d " % (i.idx))
                # fo.write("%d(%d %d)%d$ " % (i.idx, i.x, i.y, i.earn))            # ATTENTION

            fo.write("%d\n" % packs[-1].idx)
            # fo.writelines("%d(%d %d)%d$\n" % (packs[-1].idx, packs[-1].x, packs[-1].y, packs[-1].earn))  # ATTENTION


# MIN FUNCTIONS
def f(garage, packets):
    income = 0
    for i in packets:
        income += i.earn

    length = 0
    l = [garage] + packets
    for i in range(len(packets)):
        length += l[i] - l[i+1]

    # no need to plus 10 because of |fi - fj|
    loss = length / 2.0 #+ 10 #ATTENTION

    return income - loss

def minfunction(garage, workerassignment):
    fworker = []
    for i in workerassignment:
        fworker.append(f(garage, i))

    delta = max(fworker) - min(fworker)
    return delta, fworker


# INIT
def naiveassign(packets, numworkers, numpackets):
    worker = []
    random.shuffle(packets)

    for i in range(numworkers):
        buff = []
        for _ in range(numpackets//numworkers):
            buff.append(packets.pop())
        worker.append(buff)

    for i in range(numworkers):
        if packets:
            worker[i].append(packets.pop())
        else:
            break

    return worker

####################################################################################################
####################################################################################################
def climbbruteforce(delta, garage, worker):
    wl = len(worker)

    for workerid in range(wl):
        # self shuffle: swap places
        iwl = len(worker[workerid])

        for i, j in combinations(range(iwl), 2):
            b = worker[workerid][i]
            worker[workerid][i] = worker[workerid][j]
            worker[workerid][j] = b

            d, _ = minfunction(garage, worker)
            if d < delta:
                return True
            
            # swap back
            b = worker[workerid][i]
            worker[workerid][i] = worker[workerid][j]
            worker[workerid][j] = b


        # other shuffle:
        # not doing with last worker
        if workerid == wl-1:
            break
        
        # other things: swap
        for nextworker in range(workerid + 1, wl):
            iwl = list(range(len(worker[workerid])))
            random.shuffle(iwl)
            for i in iwl:
                nwl = list(range(len(worker[nextworker])))
                random.shuffle(nwl)
                for j in nwl:
                    b = worker[workerid][i]
                    worker[workerid][i] = worker[nextworker][j]
                    worker[nextworker][j] = b

                    d, _ = minfunction(garage, worker)
                    if d < delta:
                        return True

                    # swap back
                    b = worker[workerid][i]
                    worker[workerid][i] = worker[nextworker][j]
                    worker[nextworker][j] = b

        # other things: give 
        nwk = list(range(workerid + 1, wl))
        random.shuffle(nwk)
        for nextworker in nwk:
            iwl = list(range(len(worker[workerid])))
            random.shuffle(iwl)
            for i in iwl:
                nwl = list(range(len(worker[nextworker]) + 1))
                random.shuffle(nwl)
                for j in nwl:
                    
                    worker[nextworker].insert(j, worker[workerid].pop(i))

                    d, _ = minfunction(garage, worker) 
                    if d < delta:
                        return True

                    # swap back
                    worker[workerid].insert(i, worker[nextworker].pop(j))

    return False

def bruteforce(garage, worker, numworkers, numpackets):
    while True:
        delta, _ = minfunction(garage, worker)

        c = climbbruteforce(delta, garage, worker)
        if not c: # cant climb more
            return


def p(w):
    for i in w:
        print("w:")
        for j in i:
            print(j," ", end="")
        print("\n")

# MAIN PHASE
def assign(file_input, file_output):
    # read input
    garage, numworkers, numpackets, packets = readinput(file_input)
    if numworkers > numpackets:
        print("Too many workers!")
        return

    # read packages:
    # for i in packets:
    #     print(i)

    worker = naiveassign(packets, numworkers, numpackets)
    # worker = [[packets[1], packets[3], packets[2]],
    #           [packets[4], packets[0]]]
   
    # run algorithm
    # ...
    start = time.time()
    bruteforce(garage, worker, numworkers, numpackets)
    end = time.time()

    # show some answer
    val, _ = minfunction(garage, worker)
    print(val)
    print("time elapsed: ", end - start)

    
    # result running 20 workers 200 packets:
    # 0.07658131272953028
    # time elapsed:  163.59778833389282

    # write output
    writeoutput(file_output, worker)
    return


assign('in.txt', 'out.txt')
