import random, sys

def testgen(filename, worker, packet):
    with open(filename, 'w') as f:
        f.writelines("0 0\n")
        f.writelines(str(worker) + " " + str(packet) + "\n")

        for _ in range(packet):
            f.writelines(str(random.choice(range(100))) + " " + str(random.choice(range(100)))\
                + " " + str(5 + random.choice(range(100))) + " 0\n")

if __name__ == "__main__":
    testgen("input.txt", int(sys.argv[1]), int(sys.argv[2]))