import random
import time


class NQueens:
    def __init__(self,N):
        # self.board = self.getNewBoard(N)
        self.N = N

        queenPos = []
        for i in range(N):
            queenPos = queenPos + [(i, random.randint(0, N-1))]
        self.queenPosInit = queenPos

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

    def printBoardInit(self): # print demo board
        for i in range(self.N):
            for j in range(self.N):
                if (i, j) in self.queenPosInit:
                    print('Q ', end='')
                else:
                    print('. ', end='')
            print('\n', end='')
        print('----------------------------------')


    def dfs(self):
        nodes = [self.queenPosInit]

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
        
        return None

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


    def astar(self): pass

    def troll(self):
        r = self.N % 12

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

        self.queenPosSol = list(zip(range(self.N), col))

    def hasSol(self):
        if self.queenPosSol == None:
            print("Doesnt have solution") 
        elif self.allQueensSafe(self.queenPosSol):
            print("Has solution")
        else:
            print("Wrong solution")
            


                
if __name__ == "__main__":
    N = int(input())
    q = NQueens(N)

    start_time = time.time()
    q.troll()
    end_time = time.time()
    q.hasSol()

    q.printBoard()
    print("Time elapsed: %s" % (end_time - start_time))

    # for i in range(10):
    #     q = NQueens(N)
    #     q.printBoardInit()