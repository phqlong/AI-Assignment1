import random
import numpy as np


class NQueens:
    def __init__(self, n):
        self.board, self.queenPositions = self.getNewBoard(n)
        self.n = n

    def getNewBoard(self, n):
        # queens are represented as ones in 2d list of all zeros
        # Since it's a 2d list, each element is a row of zeros except for the queen
        board = []
        queensPos = []

        # makes n x n board of zeros
        for x in range(n):
            board.append([0]*n)

        # sets a random value of each row to be 1, denoting the queen
        for x in range(n):
            randomIndex = random.randint(0, n-1)
            board[x][randomIndex] = 1
            queensPos.append((x, randomIndex))

        return (board, queensPos)

    # returns true if problem is solved and all queens safe, false otherwise
    def isAllQueensSafe(self):
        for pos in self.queenPositions:
            if(self.isUnderAttack(pos)):
                return False
        return True

    # check if pos has a queen, then return true if queen is under attack
    def isUnderAttack(self, pos):
        for queen in self.queenPositions:
            # last inqueality checks to make sure you arent comparing the same queen
            if (queen == pos):
                continue

            # attack via Collumn
            if (pos[1] == queen[1]):
                return True

            # attack via Row
            if (pos[0] == queen[0]):
                return True

            # attack via Diagonal
            if (abs(queen[0] - pos[0]) == abs(queen[1] - pos[1])):
                return True

        return False

    # returns number of pieces attacking queen at position pos
    def numQueenConflicts(self, pos):
        # checks to make sure given position is a queen
        assert pos in self.queenPositions
        count = 0
        for queen in self.queenPositions:
            if (queen == pos):
                continue

            if (abs(queen[0] - pos[0]) == abs(queen[1] - pos[1])):
                count += 1

            if (pos[0] == queen[0]):
                count += 1

            if (pos[1] == queen[1]):
                count += 1

        return count

    # returns position of random queen
    def pickRandomQueen(self):
        newIndex = random.randint(0, self.n - 1)
        return self.queenPositions[newIndex]

    # prints out all positions of queens
    def printBoard(self):
        for queen in self.queenPositions:
            print(queen)

    # moves queen from startpos to endpos
    def moveQueen(self, startPos, endPos):
        # assert fail if the start position does not have a queen
        assert self.board[startPos[0]][startPos[1]] == 1

        self.board[startPos[0]][startPos[1]] = 0
        self.board[endPos[0]][endPos[1]] = 1
        self.queenPositions.remove(startPos)
        self.queenPositions.append(endPos)

    def availablePositions(self, pos):
        # returns list of tuples with all positions queen can go
        availablePos = []
        for x in range(self.n):
            availablePos.append((pos[0], x))

        return availablePos


def NQueens_min_conflicts(n):
    # min conflicts solver for NQueens problems

    NQ = NQueens(n)
    # timer = 0
    while(not NQ.isAllQueensSafe()):
        # n + 1 is greater than any possibility of attacks so this is guaranteed to get minimized
        minAttacks = n + 1
        pickedQueen = NQ.pickRandomQueen()

        positions = NQ.availablePositions(pickedQueen)
        minConflictPosition = (-1, -1)

        # iterate through all positions of pickedQueen and move to position of minimum conflict
        for pos in positions:
            NQ.moveQueen(pickedQueen, pos)

            newNumberOfConflicts = NQ.numQueenConflicts(pos)
            if(newNumberOfConflicts < minAttacks):
                minConflictPosition = pos
                minAttacks = newNumberOfConflicts

            NQ.moveQueen(pos, pickedQueen)  # move queen back

        # move queen to least conflict spot
        NQ.moveQueen(pickedQueen, minConflictPosition)

    print(NQ.printBoard())
    board = np.array(NQ.board)
    print(board)


if __name__ == "__main__":
    NQueens_min_conflicts(8)
