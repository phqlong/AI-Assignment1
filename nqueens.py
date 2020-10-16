import random
import numpy as np
import time


class NQueens:
    def __init__(self, n):
        self.queenPositions = self.getNewBoard(n)
        self.N = n

    def getNewBoard(self, n):
        # sets a random value of each row to be 1, denoting the queen
        queensPos = random.sample(range(0, n), n)
        # queensPos = [-1]*n
        return queensPos

    # returns true if problem is solved and all queens safe, false otherwise
    def isAllQueensSafe(self):
        for row in range(self.N):
            if(self.isUnderAttack((row, self.queenPositions[row]))):
                return False
        return True

    # check if pos has a queen, then return true if queen is under attack
    def isUnderAttack(self, pos):
        # checks to make sure given position is a queen
        # assert queenCol == self.queenPositions[queenRow]

        queenRow, queenCol = pos
        for otherQueenRow in range(self.N):
            # checks not comparing the same queen
            if (otherQueenRow == queenRow):
                continue

            otherQueenCol = self.queenPositions[otherQueenRow]
            if(otherQueenCol == -1):
                continue

            # attack via Row
            if (queenRow == otherQueenRow):
                return True

            # attack via Collumn
            if (queenCol == otherQueenCol):
                return True

            # attack via Diagonal
            if (abs(queenRow - otherQueenRow) == abs(queenCol - otherQueenCol)):
                return True

        return False

    # check if pos has a queen, then returns number of conflicts with that queen
    def numQueenConflicts(self, pos):
        # checks to make sure given position is a queen
        # assert queenCol == self.queenPositions[queenRow]
        queenRow, queenCol = pos
        count = 0

        for otherQueenRow in range(self.N):
            # checks not comparing the same queen
            if (otherQueenRow == queenRow):
                continue

            otherQueenCol = self.queenPositions[otherQueenRow]

            # attack via Row
            if (queenRow == otherQueenRow):
                count += 1

            # attack via Collumn
            if (queenCol == otherQueenCol):
                count += 1

            # attack via Diagonal
            if (abs(queenRow - otherQueenRow) == abs(queenCol - otherQueenCol)):
                count += 1

        return count

    # returns position: (row, col) of arbitary queen from the board
    def pickRandomQueen(self):
        randomRow = random.randint(0, self.N - 1)
        return (randomRow, self.queenPositions[randomRow])

    # prints out all positions of queens
    def printQueensPos(self):
        for row in range(self.N):
            print((row, self.queenPositions[row]))

    # prints out the board
    def printBoard(self):
        for row in range(self.N):
            for col in range(self.N):
                if self.queenPositions[row] == col:
                    print('Q ', end=''),
                else:
                    print('. ', end=''),
            print()

    # max_N = 21 => recursion
    def NQueens_DFS(self, row):
        while row < self.N:
            col = self.queenPositions[row] + 1
            # print((row, col))

            while col < self.N:
                # check if this col is underAttack
                if self.isUnderAttack((row, col)):
                    # next col
                    col = col + 1
                else:
                    # this (row, col) is safe
                    self.queenPositions[row] = col
                    row = row + 1
                    break

            # Backtracking
            # All col in this row has visited
            # => backtrack to row-1
            if col == self.N:
                self.queenPositions[row] = -1
                # return self.NQueens_DFS(row - 1)
                row = row - 1

        # Goal
        if row == self.N:
            print('Finished!')
            return True

    def NQueens_min_conflicts(self):
        # min conflicts solver for NQueens problems

        while(not self.isAllQueensSafe()):
            pickedQueen = self.pickRandomQueen()

            # n+1 is greater than any possibility of attacks so this is guaranteed to get minimized
            minAttacks = self.N + 1
            minConflictCol = -1

            # iterate through all positions of pickedQueen and move to position of minimum conflict
            for newCol in range(self.N):
                # move queen to newCol
                self.queenPositions[pickedQueen[0]] = newCol

                numConflicts = self.numQueenConflicts((pickedQueen[0], newCol))
                if(numConflicts < minAttacks):
                    minConflictCol = newCol
                    minAttacks = numConflicts

                # move queen back
                self.queenPositions[pickedQueen[0]] = pickedQueen[1]

            # move queen to least conflict spot
            self.queenPositions[pickedQueen[0]] = minConflictCol


if __name__ == "__main__":
    start_time = time.time()

    NQ = NQueens(40)
    NQ.NQueens_DFS(0)
    # NQ.NQueens_min_conflicts()

    # NQ.printQueensPos()
    NQ.printBoard()
    print("--- %s seconds ---" % (time.time() - start_time))
