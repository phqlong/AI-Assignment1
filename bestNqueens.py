"""
                                N-Queens problem 
                                ----------------
    State-space representation:
        State: 
            Queen-Position list contain N 2-tuples: (row, col) with row and col in range from 0 to N-1
        Initial state: 
            Queen-Position list is empty
        Goal state: 
            List of all N queen's position such that no two are in the same row, column, or diagonal.
        Next step state: 
            Place position for one more queen and append to Queen-Position list.

    All using algorithm:
        DFS algorithm
        BrFS algorithm
        Heuristic algorithm: Our super-pro optimized algorithm (similar to hill climbing) for N = 100.000 in 10 -> 15 minutes
"""

import random
import time
from itertools import combinations


class NQueens:
    def __init__(self, N):
        self.N = N
        self.queenPosSol = None

    ########################################################################################
    ''' Rule checker '''

    # check for row violate exists
    def checkRowViolate(self, queenPos, N):
        col = [0] * N
        for i in range(len(queenPos)):
            col[queenPos[i][0]] += 1
            if col[queenPos[i][1]] > 1:
                return True
        return False

    # check for Collumn violate exists
    def checkColViolate(self, queenPos, N):
        col = [0] * N
        for i in range(len(queenPos)):
            col[queenPos[i][1]] += 1
            if col[queenPos[i][1]] > 1:
                return True
        return False

    # check for positive diagonal violate exists
    def checkPosDiagViolate(self, queenPos, N):
        diag = [0] * (2*N - 1)
        for i in range(len(queenPos)):
            diag[queenPos[i][0] + queenPos[i][1]] += 1
            if diag[queenPos[i][0] + queenPos[i][1]] > 1:
                return True
        return False

    # check for negative diagonal violate exists
    def checkNegDiagViolate(self, queenPos, N):
        diag = [0] * (2*N - 1)
        for i in range(len(queenPos)):
            diag[queenPos[i][0] - queenPos[i][1]] += 1
            if diag[queenPos[i][0] - queenPos[i][1]] > 1:
                return True
        return False

    # return True if exists any violation
    def isNotSafe(self, queenPos):
        if self.checkRowViolate(queenPos, self.N):
            return True
        if self.checkColViolate(queenPos, self.N):
            return True
        if self.checkPosDiagViolate(queenPos, self.N):
            return True
        if self.checkNegDiagViolate(queenPos, self.N):
            return True
        return False

    # check right, wrong or no solution
    def checkSolution(self):
        if self.queenPosSol == None:
            print("Doesnt have solution")
        elif not self.isNotSafe(self.queenPosSol):
            print("Has right solution")
        else:
            print("Wrong solution")

    ###########################################################################################
    ''' Utility '''

    # prints out all positions of queens
    def printQueen(self):
        if self.queenPosSol == None:
            print("No solution")
            return

        for i in range(self.N):
            print((self.queenPosSol[i]))

    # print demo board for N < 50
    def printBoard(self):
        if self.queenPosSol == None:
            print("No solution")
            return

        for i in range(self.N):
            for j in range(self.N):
                if (i, j) in self.queenPosSol:
                    print('Q ', end='')
                else:
                    print('. ', end='')
            print('\n', end='')

    ###########################################################################################
    ''' Depth-first search algorithm - DFS '''

    def dfs(self):
        nodes = [[]]

        while nodes != []:
            pos = nodes.pop()
            queennum = len(pos)

            # shuffle range for better performance
            l = list(range(self.N))
            random.shuffle(l)

            for i in l:
                sample = pos + [(queennum, i)]
                if not self.isNotSafe(sample):
                    if (len(sample) == self.N):
                        self.queenPosSol = sample
                        return

                    nodes.append(sample)

        return

    ###########################################################################################
    ''' Breadth-first search algorithm - BrFS '''
    # bfs too slow, n=11: 37.5s
    # because solution is at the bottom of the tree

    def bfs(self):
        nodes = [[]]

        while nodes != []:
            pos = nodes.pop(0)
            queennum = len(pos)

            # shuffle range for better performance
            l = list(range(self.N))
            random.shuffle(l)

            for i in l:
                sample = pos + [(queennum, i)]
                if not self.isNotSafe(sample):
                    if (len(sample) == self.N):
                        self.queenPosSol = sample
                        return

                    nodes.append(sample)

        return

    ###########################################################################################
    ''' 
            Heuristic algorithm                                 
    Fast search algorithm (similar to hill climbing)     
    for N = 100.000 in 7 -> 15 minutes, belongs to configuration of processor   
    Plz stay calm and our algorithm won't let you down!!! :D
    '''

    def calcCollision(self, queencol, dp, dn):
        for i in range(self.N):
            dp[i] = 0
            dn[i] = 0

        collision = 0

        for i in range(self.N):
            dp[i + queencol[i]] += 1
            dn[i - queencol[i]] += 1

        for i in range(self.N * 2 - 1):
            if dp[i] > 1:
                collision += dp[i] - 1
            if dn[i] > 1:
                collision += dn[i] - 1

        return collision

    def calcAttack(self, queencol, dp, dn, atk):
        num_of_atk = 0
        for i in range(len(queencol)):
            if dp[i + queencol[i]] > 1:
                atk[num_of_atk] = i
                num_of_atk += 1
            elif dn[i - queencol[i]] > 1:
                atk[num_of_atk] = i
                num_of_atk += 1

        return num_of_atk

    def isSwapOK(self, i, j, queencol, dp, dn):
        if i == j:
            return False

        # ori: i, q[i] and j, q[j]; new: j, q[i] and i, q[j]
        dpiiori = dp[i + queencol[i]]
        dpjjori = dp[j + queencol[j]]
        dniiori = dn[i - queencol[i]]
        dnjjori = dn[j - queencol[j]]

        dpijori = dp[i + queencol[j]]
        dpjiori = dp[j + queencol[i]]
        dnijori = dn[i - queencol[j]]
        dnjiori = dn[j - queencol[i]]

        oriarr = [dpiiori, dpjjori, dniiori, dnjjori,
                  dpijori, dpjiori, dnijori, dnjiori]

        dpiinew = dpiiori - 1
        dpjjnew = dpjjori - 1
        dniinew = dniiori - 1
        dnjjnew = dnjjori - 1

        dpijnew = dpijori + 1
        dpjinew = dpjiori + 1
        dnijnew = dnijori + 1
        dnjinew = dnjiori + 1

        newarr = [dpiinew, dpjjnew, dniinew, dnjjnew,
                  dpijnew, dpjinew, dnijnew, dnjinew]

        cori = self.collupd(oriarr, [])
        cnew = self.collupd(newarr, [])

        if cori > cnew:
            return True
        else:
            return False

    def makeSwap(self, i, j, queencol, dp, dn):
        dp[i + queencol[i]] -= 1
        dp[j + queencol[j]] -= 1
        dn[i - queencol[i]] -= 1
        dn[j - queencol[j]] -= 1

        dp[i + queencol[j]] += 1
        dp[j + queencol[i]] += 1
        dn[i - queencol[j]] += 1
        dn[j - queencol[i]] += 1

        buffer = queencol[i]
        queencol[i] = queencol[j]
        queencol[j] = buffer

        collision = self.collupd(dp, dn)
        return collision

    def collupd(self, dp, dn):
        r = 0
        for i in dp:
            if i > 1:
                r += i-1
        for i in dn:
            if i > 1:
                r += i-1
        return r

    # run for ~15 mins
    def queen_fast_search(self):
        C1 = 0.45
        C2 = 32
        collision = -1

        while collision != 0:
            # Initialize random queen collumn as a sample list
            queencol = random.sample(range(0, self.N), self.N)

            dp = [0] * (self.N * 2 - 1)
            dn = [0] * (self.N * 2 - 1)
            atk = [0] * self.N

            collision = self.calcCollision(queencol, dp, dn)
            if collision == 0:
                break

            limit = C1 * collision
            num_of_atk = self.calcAttack(queencol, dp, dn, atk)
            loopcount = 0

            while loopcount <= C2 * self.N:

                for k in range(num_of_atk):
                    i = atk[k]
                    j = random.choice(range(self.N))
                    # print(i, j)

                    if self.isSwapOK(i, j, queencol, dp, dn):
                        collision = self.makeSwap(i, j, queencol, dp, dn)

                        if collision == 0:
                            self.queenPosSol = list(
                                zip(range(self.N), queencol))
                            return
                        elif collision < limit:
                            limit = C1 * collision
                            num_of_atk = self.calcAttack(
                                queencol, dp, dn, atk)

                loopcount = loopcount + num_of_atk

        self.queenPosSol = list(zip(range(self.N), queencol))


if __name__ == "__main__":
    N = int(input())
    q = NQueens(N)

    start_time = time.time()
    q.queen_fast_search()
    # q.dfs()
    q.printBoard()

    q.checkSolution()
    end_time = time.time()
    print("Time elapsed: %s" % (end_time - start_time))
