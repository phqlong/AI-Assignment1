import random
import numpy as np
import time


class NQueens:
    def __init__(self, n):
        self.N = 0
        self.queenPositions = []
        self.getNewBoard(n)

    def getNewBoard(self, n):
        # sets a random value of each row to be 1, denoting the queen
        # queensPos = random.sample(range(0, self.N), self.N
        # queensPos = [-1]*n

        # This def wil append ideal col in each queenPosition[row]
        for row in range(n):

            # Initilize min conflicts in a row is max: N + 1
            # Candidate list saves collumns have min_conflict
            min_conflict = self.N + 1
            candidates = []

            # Firstly, start with col = 0 in each row
            self.queenPositions.append(0)
            self.N = self.N + 1

            # Finds collumns have min_conflict and adds them to the candidates
            for col in range(n):
                self.queenPositions[row] = col
                numConflicts = self.numQueenConflicts(
                    (row, self.queenPositions[row]))

                if numConflicts == min_conflict:
                    candidates.append(col)
                elif numConflicts < min_conflict:
                    candidates = []
                    candidates.append(col)
                    min_conflict = numConflicts

            # Selects a random col from candidates which have min_conflict
            self.queenPositions[row] = random.choice(candidates)

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

    # Test N = 40 => Min_time = 5s - Avg_time = 20s - Max_time > 1 min
    def NQueens_DFS(self):
        numMoves = 0

        row = 0
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

            numMoves += 1

        # Goal
        if row == self.N:
            print('Finished!')
        
        return numMoves

    def NQueens_min_conflicts(self):
        # min conflicts solver for NQueens problems
        numMoves = 0

        while not self.isAllQueensSafe():
            row, col = self.pickRandomQueen()

            # Check if picked queen is safe
            if not self.isUnderAttack((row, col)):
                continue

            # Initilize min conflicts in a row is max: N + 1
            # Candidate list saves collumns have min_conflict
            min_conflict = self.N + 1
            candidates = []

            # Finds collumns have min_conflict and adds them to the candidates
            for newCol in range(self.N):
                self.queenPositions[row] = newCol
                numConflicts = self.numQueenConflicts((row, self.queenPositions[row]))

                if numConflicts == min_conflict:
                    candidates.append(newCol)
                elif numConflicts < min_conflict:
                    candidates = []
                    candidates.append(newCol)
                    min_conflict = numConflicts

            # Selects a random col from candidates which have min_conflict
            self.queenPositions[row] = random.choice(candidates)

            numMoves += 1
        
        return numMoves


if __name__ == "__main__":
    start_time = time.time()

    NQ = NQueens(100)
    # NQ.printBoard()

    # numMoves = NQ.NQueens_DFS()
    numMoves = NQ.NQueens_min_conflicts()

    NQ.printQueensPos()
    # NQ.printBoard()
    print("--- %s moves -- %s seconds ---" %(numMoves, (time.time() - start_time)))
