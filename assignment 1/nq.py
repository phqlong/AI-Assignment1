import random
import time

# math descr
# because queens live on theirs own row, queen pos denote its (row,column)
class NQueens:
    def __init__(self,N):
        # self.board = self.getNewBoard(N)
        self.N = N
        self.queenPosSol  = None

    def allQueensSafe(self, queenPos): # returns true if problem is solved and all queens safe, false otherwise
        for pos in queenPos:
            if(self.UnderAttack(queenPos, pos)):
                return False
        return True

    def attackViaCol(self, queenPos, pos):
        for queen in queenPos:
            if(pos[1] == queen[1] and queen != pos): # last inqueality checks to make sure you arent comparing the same queen
                return True
        return False

    def attackViaRow(self, queenPos, pos):
        # for queen in queenPos:
        #     if(pos[0] == queen[0] and queen != pos):
        #         return True
        return False

    def attackViaDiagonal(self, queenPos, pos):
        for queen in queenPos:
            if (abs(queen[0] - pos[0]) == abs(queen[1] - pos[1]) and queen != pos):
                return True
        return False

    def UnderAttack(self, queenPos, position):
        if(self.attackViaDiagonal(queenPos, position)):
            return True
        if(self.attackViaRow(queenPos, position)):
            return True
        if(self.attackViaCol(queenPos, position)):
            return True
        return False


    def printQueen(self): # prints out all positions of queens
        if self.queenPosSol == None:
            print("No solution")
            return

        for i in range(self.N):
            print((self.queenPosSol[i]))


    def printBoard(self):
        if self.queenPosSol == None:
            print("No solution")
            return

        for i in range(self.N):
            for j in range(self.N):
                if j == self.queenPosSol[i][1]:
                    print('Q ', end='')
                else:
                    print('. ', end='')
            print('\n', end='')


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
                if self.allQueensSafe(sample):
                    if (len(sample) == self.N):
                        self.queenPosSol = sample
                        return

                    nodes.append(sample)
        
        return

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
                if self.allQueensSafe(sample):
                    if (len(sample) == self.N):
                        self.queenPosSol = sample
                        return

                    nodes.append(sample)
        
        return

                
if __name__ == "__main__":
    N = int(input())
    q = NQueens(N)

    start_time = time.time()
    q.dfs()
    end_time = time.time()

    q.printQueen()
    q.printBoard()
    print("Time elapsed: %s" % (end_time - start_time))