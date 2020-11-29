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

class SolutionStorage():
    def __init__(self):
        self.good = None
        self.sollist = []


    def setmax(self, garage, worker):
        if self.good == None:
            self.good, _ = minfunction(garage, worker)
            self.sollist = []
            for i in worker:
                self.sollist.append([j.idx for j in i])

        else:
            good, _ = minfunction(garage, worker)
            if self.good > good:
                self.sollist = []
                for i in worker:
                    self.sollist.append([j.idx for j in i])

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
def writeoutput(filename, sol):
    with open(filename, 'w') as fo:
        for lines in sol.sollist:
            for i in lines[:-1]:
                fo.write("%d " % i)
            fo.write("%d\n" % lines[-1])


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
    loss = length / 2.0

    return income - loss

def minfunction(garage, workerassignment):
    fworker = []
    for i in workerassignment:
        fworker.append(f(garage, i))

    delta = max(fworker) - min(fworker)
    return delta, fworker

def key(a):
    return a[1]

def minfunction2(garage, workerassignment):
    fworker = []
    for i in range(len(workerassignment)):
        fworker.append((i, f(garage, workerassignment[i])))

    minf = max(fworker, key=key)[1] - min(fworker, key=key)[1]
    return minf, fworker

# INIT
def naiveassign(packets, numworkers, numpackets):
    p = packets.copy()
    worker = []
    random.shuffle(p)

    for i in range(numworkers):
        buff = []
        for _ in range(numpackets//numworkers):
            buff.append(p.pop())
        worker.append(buff)

    for i in range(numworkers):
        if p:
            worker[i].append(p.pop())
        else:
            break

    return worker

####################################################################################################
####################################################################################################
def cutthrough(fworker, worker):
    maxlist = []
    maxval = max(fworker, key=key)[1]
    maxlist = [i for i in fworker if i[1] == maxval]

    minlist = []

    if fworker:
        minval = min(fworker, key=key)[1]
        minlist = [i for i in fworker if i[1] == minval]

    delta = maxlist[0][1] - minlist[0][1]
    return delta, maxlist, minlist
    

def climb(fval, delta, garage, worker, maxlist, minlist):
    # min inner swap
    # not needed for value-only
    mincap = minlist[0][1]
    maxcap = maxlist[0][1]

    for minw, _ in minlist:
        n = len(worker[minw])
        for i in range(n - 1):
            for j in range(i + 1, n):
                buffmin = worker[minw].copy()

                buff = buffmin[i]
                buffmin[i] = buffmin[j]
                buffmin[j] = buff

                newmin = f(garage, buffmin)
                # print("newmin:", newmin)
                if mincap < newmin and newmin <= maxcap:
                    worker[minw] = buffmin
                    # print("min swap worth")
                    return True



    # min max swap
    for minw, _ in minlist:
        for maxw, _ in maxlist:
            for minidx in range(len(worker[minw])):
                for maxidx in range(len(worker[maxw])):
                    buffmin = worker[minw].copy()
                    buffmax = worker[maxw].copy()

                    buff = buffmin[minidx]
                    buffmin[minidx] = buffmax[maxidx]
                    buffmax[maxidx] = buff

                    newdelta = abs(f(garage, buffmax) - f(garage, buffmin))
                    if newdelta < delta:
                        worker[minw] = buffmin
                        worker[maxw] = buffmax
                        # print("min max worth")
                        return True

    # max min give
    for maxw, _ in maxlist:
        for minw, _ in minlist:
            for maxidx in range(len(worker[maxw])):
                buffmin = worker[minw].copy()
                buffmax = worker[maxw].copy()

                buffmin.append(buffmax.pop(maxidx))
                newdelta = abs(f(garage, buffmax) - f(garage, buffmin))
                if newdelta < delta:
                    worker[minw] = buffmin
                    worker[maxw] = buffmax
                    # print("max min worth")
                    return True

    # max inner swap (not good for 1 big max) (not needed for value only)
    # if the biggest is not alone, then we shall shuffle that worker path
    # print("fval:", fval, "max-min",maxcap - mincap)
    # if maxcap - mincap == fval:
    for maxw, _ in maxlist:
        # print(worker)
        n = len(worker[maxw])
        # print(n)
        for i in range(n - 1):
            for j in range(i + 1, n):
                buffmax = worker[maxw].copy()

                buff = buffmax[i]
                buffmax[i] = buffmax[j]
                buffmax[j] = buff

                newmax = f(garage, buffmax)
                # print("new max:", newmax, "max:", maxcap)
                if mincap <= newmax and newmax < maxcap:
                    worker[maxw] = buffmax
                    # print("max swap worth")
                    return True
    # print("idle")
    return False

def climbfast(garage, worker, numworkers, numpackets):
    while True:
        fval, fworker = minfunction2(garage, worker)
        delta, maxlist, minlist = cutthrough(fworker, worker)

        c = climb(fval, delta, garage, worker, maxlist, minlist)
        if not c: # cant climb more
            return

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

def climbslow(garage, worker, numworkers, numpackets):
    while True:
        delta, _ = minfunction(garage, worker)

        c = climbbruteforce(delta, garage, worker)
        if not c: # cant climb more
            return

# MAIN PHASE
def assign(file_input, file_output):
    # read input
    garage, numworkers, numpackets, packets = readinput(file_input)
    if numworkers > numpackets:
        print("Too many workers!")
        return
   
    # run algorithm
    w = SolutionStorage()

    start = time.time()

    if numpackets <= 150:
        worker = naiveassign(packets, numworkers, numpackets)
        climbslow(garage, worker, numworkers, numpackets)
        w.setmax(garage, worker)

    elif numpackets <= 500:
        for _ in range(5):
            worker = naiveassign(packets, numworkers, numpackets)
            climbfast(garage, worker, numworkers, numpackets)
            w.setmax(garage, worker)
        
    elif numpackets <= 2000:
        for _ in range(2):
            worker = naiveassign(packets, numworkers, numpackets)
            climbfast(garage, worker, numworkers, numpackets)
            w.setmax(garage, worker)

    else:
        worker = naiveassign(packets, numworkers, numpackets)
        climbfast(garage, worker, numworkers, numpackets)
        w.setmax(garage, worker)

    end = time.time()

    # show some answer
    val, _ = minfunction(garage, worker)
    print(val)
    print("time elapsed: ", end - start)


    # write output
    writeoutput(file_output, w)
    return


assign('input.txt', 'output.txt')
