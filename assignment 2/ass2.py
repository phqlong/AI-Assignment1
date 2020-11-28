# Them cac thu vien neu can
import math
import random



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
        return "pack idx: " + str(self.idx) + "loc: " + str(self.x) + ", " \
            + str(self.y) + ", income: " + str(self.earn)


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
                fo.write("%d(%d %d) " % (i.idx, i.x, i.y))            # ATTENTION

            fo.writelines("%d(%d %d)\n" % (packs[-1].idx, packs[-1].x, packs[-1].y))  # ATTENTION


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
    loss = length * 10 / 20 #+ 10 #ATTENTION
    # loss = 0
    # income = 0                  # ATTENTION
    return income - loss

def key(a):
    return a[1]

def minfunction(garage, workerassignment):
    fworker = []
    for i in range(len(workerassignment)):
        fworker.append((i, f(garage, workerassignment[i])))

    # minval = min(fworker, key=key)[1]
    # for i in range(len(fworker)):
    #     fworker[i] = (fworker[i][0], fworker[i][1] - minval)

    minf = max(fworker, key=key)[1] - min(fworker, key=key)[1]
    return minf, fworker


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

    # for i in range(numworkers):
    #     print("worker",i,"has:")
    #     for j in worker[i]:
    #         print("   ",j)

    return worker


# ALGO
def cutthrough(fworker, worker):
    maxlist = []
    maxval = max(fworker, key=key)[1]
    maxlist = [i for i in fworker if i[1] == maxval]
    # while True:
    #     maxval = max(fworker, key=key)[1]
    #     maxlist = [i for i in fworker if i[1] == maxval]
    #     for i in maxlist:
    #         if len(worker[i[0]]) == 1:
    #             fworker.remove(i)
    #             maxlist.remove(i)

    #     if maxlist or not fworker:
    #         break

    minlist = []

    if fworker:
        minval = min(fworker, key=key)[1]
        minlist = [i for i in fworker if i[1] == minval]

    delta = maxlist[0][1] - minlist[0][1]
    print("maxlist: ", maxlist)
    print("minlist: ", minlist)
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
                print("newmin:", newmin)
                if mincap < newmin and newmin <= maxcap:
                    worker[minw] = buffmin
                    print("min swap worth")
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
                        print("min max worth")
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
                    print("max min worth")
                    return True

    # max inner swap (not good for 1 big max) (not needed for value only)
    # if the biggest is not alone, then we shall shuffle that worker path
    # print("fval:", fval, "max-min",maxcap - mincap)
    # if maxcap - mincap == fval:
    for maxw, _ in maxlist:
        print(worker)
        n = len(worker[maxw])
        print(n)
        for i in range(n - 1):
            for j in range(i + 1, n):
                buffmax = worker[maxw].copy()

                buff = buffmax[i]
                buffmax[i] = buffmax[j]
                buffmax[j] = buff

                newmax = f(garage, buffmax)
                print("new max:", newmax, "max:", maxcap)
                if mincap <= newmax and newmax < maxcap:
                    worker[maxw] = buffmax
                    print("max swap worth")
                    return True
    print("idle")
    return False

def algo(garage, worker, numworkers, numpackets):
    minworker = None
    
    while True:
        fval, fworker = minfunction(garage, worker)
        print("fworker: ", fworker)
        delta, maxlist, minlist = cutthrough(fworker, worker)

        # if not maxlist or not minlist:
        #     minworker = worker.copy()
        #     break

        c = climb(fval, delta, garage, worker, maxlist, minlist)
        if not c: # cant climb more
            minworker = worker.copy()
            break
    # while True:
    #     maxval = max(fworker)
    #     maxlist = [i for i, j in enumerate(fworker) if j == maxval]
    #     minval = min(fworker)
    #     minlist = [i for i, j in enumerate(fworker) if j == minval]

    #     for i in maxlist:
    #         if len(worker[i]) == 1:
    #             maxlist.remove(i)

        
    return minworker


# MAIN PHASE
def assign(file_input, file_output):
    # read input
    garage, numworkers, numpackets, packets = readinput(file_input)
    if numworkers > numpackets:
        print("Too many workers!")
        return

    worker = naiveassign(packets, numworkers, numpackets)
    # worker = [[packets[0]],[packets[2], packets[1]]]
   
    # run algorithm
    # ...
    worker = algo(garage, worker, numworkers, numpackets)


    # show some answer
    val, w = minfunction(garage, worker)
    print(val)
    print(w)


    # write output
    writeoutput(file_output, worker)
    return


assign('in.txt', 'out.txt')
