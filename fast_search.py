import random
import time
from itertools import combinations


class NQueens:
    def __init__(self,N):
        self.N = N
        self.queenPosSol  = None

    ############################################
    # rule checker
    def rowviolate(self, queenPos, N):
        col = [0] * N
        for i in range(len(queenPos)):
            col[queenPos[i][0]] += 1
            if col[queenPos[i][1]] > 1:
                return True
        return False

    def colviolate(self, queenPos, N):
        col = [0] * N
        for i in range(len(queenPos)):
            col[queenPos[i][1]] += 1
            if col[queenPos[i][1]] > 1:
                return True
        return False

    def diagplusviolate(self, queenPos, N):
        diag = [0] * (2*N - 1)
        for i in range(len(queenPos)):
            diag[queenPos[i][0] + queenPos[i][1]] += 1
            if diag[queenPos[i][0] + queenPos[i][1]] > 1:
                True
        return False

    def diagminusviolate(self, queenPos, N):
        diag = [0] * (2*N - 1)
        for i in range(len(queenPos)):
            diag[queenPos[i][0] - queenPos[i][1]] += 1
            if diag[queenPos[i][0] - queenPos[i][1]] > 1:
                True
        return False

    def notsafe(self, queenPos):
        if self.rowviolate(queenPos, self.N):
            return True
        if self.colviolate(queenPos, self.N):
            return True
        if self.diagplusviolate(queenPos, self.N):
            return True
        if self.diagminusviolate(queenPos, self.N):
            return True
        return False
    
    ###############################################
    # Utility
    def printQueen(self): # prints out all positions of queens
        if self.queenPosSol == None:
            print("No solution")
            return

        for i in range(self.N):
            print((self.queenPosSol[i]))
            
    def printBoard(self): # print demo board
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

    def hasSol(self):
        if self.queenPosSol == None:
            print("Doesnt have solution") 
        elif not self.notsafe(self.queenPosSol):
            print("Has right solution")
        else:
            print("Wrong solution")

    ###############################################
    # straight solution gen
    def straight_sol(self, N):
        r = N % 12

        coleven = list(range(2, N+1, 2))
        if r == 3 or r == 9:
            coleven.append(coleven.pop(0))

        colodd = list(range(1, N+1, 2))
        
        def swapPositions(list, pos1, pos2): 
            # Storing the two elements 
            # as a pair in a tuple variable get 
            get = list[pos1], list[pos2] 
            
            # unpacking those elements 
            list[pos2], list[pos1] = get 
            
            return list

        if r == 8:
            for i in range(0, len(colodd), 2):
                swapPositions(colodd, i, i+1)
        elif r == 2:
            swapPositions(colodd, 0, 1)
            colodd.append(colodd.pop(2))
        elif r == 3 or r == 9:
            colodd.append(colodd.pop(0))
            colodd.append(colodd.pop(0))

        col = coleven + colodd
        col = list(map(lambda x: x-1, col))

        # self.queenPosSol = list(zip(range(self.N), col))
        return col

    ###############################################
    # queen fast search algorithm
    def randominit(self, N):
        queencol = list(range(N))
        random.shuffle(queencol)
        return queencol

    def compute_collision(self, queencol, dp, dn):
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

    def compute_atk(self, queencol, dp, dn, atk):
        num_of_atk = 0
        for i in range(len(queencol)):
            if dp[i + queencol[i]] > 1:
                atk[num_of_atk] = i
                num_of_atk += 1
            elif dn[i - queencol[i]] > 1:
                atk[num_of_atk] = i
                num_of_atk += 1

        return num_of_atk

    def swapok(self, i, j, queencol, dp, dn):
        if i == j:
            return False

        #ori: i, q[i] and j, q[j]; new: j, q[i] and i, q[j]
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

    def doswap(self, i, j, queencol, dp, dn):
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

    # about 782 seconds
    # run for ~15 mins
    def queen_fast_search(self, initfunc = None):
        C1 = 0.45
        C2 = 32
        collision = -1

        while collision != 0:
            if initfunc:
                queencol = initfunc(self.N)
            else:
                queencol = self.randominit(self.N)

            dp = [0] * (self.N * 2 - 1)
            dn = [0] * (self.N * 2 - 1)
            atk = [0] * self.N

            collision = self.compute_collision(queencol, dp, dn)
            if collision == 0:
                break

            limit = C1 * collision
            num_of_atk = self.compute_atk(queencol, dp, dn, atk)
            loopcount = 0
            
            # for fun
            a,b,c,d = True, True, True, True
            
            while loopcount <= C2 * self.N:

                for k in range(num_of_atk):
                    i = atk[k]
                    j = random.choice(range(self.N))
                    # print(i, j)

                    if self.swapok(i, j, queencol, dp, dn) == True:
                        collision = self.doswap(i, j, queencol, dp, dn)

                        # for fun to know how its goes
                        if collision < 5000 and a:
                            print("almost there")
                            a = False
                        elif collision < 10000 and b:
                            print("Wait for it")
                            b = False
                        elif collision < 26000 and c:
                            print("half done")
                            c = False
                        elif collision < 39000 and d:
                            print("quartered")
                            d = False

                        if collision == 0:
                            self.queenPosSol = list(zip(range(self.N), queencol))
                            return
                        elif collision < limit:
                            limit = C1 * collision
                            num_of_atk = self.compute_atk(queencol, dp, dn, atk)

                loopcount = loopcount + num_of_atk
        
        self.queenPosSol = list(zip(range(self.N), queencol))



if __name__ == "__main__":
    N = int(input())
    q = NQueens(N)

    start_time = time.time()
    q.queen_fast_search(q.straight_sol)

    q.hasSol()
    end_time = time.time()
    print("Time elapsed: %s" % (end_time - start_time))