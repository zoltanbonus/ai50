"""
Tic Tac Toe Player
"""

import math
import numpy as np
import copy
import sys

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X

    numpyBoard = np.array(board)
    xCount = np.count_nonzero(numpyBoard == X)
    oCount = np.count_nonzero(numpyBoard == O)

    if xCount > oCount:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                result.add((i, j))

    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]

    if board[i][j] != EMPTY:
        raise Exception('Invalid action')

    nextPlayer = player(board)
    newBoard = copy.deepcopy(board)
    newBoard[i][j] = nextPlayer
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # Check horizontally
        if (board[i][0] == board[i][1] == board[i][2]) and board[i][0] != EMPTY:
            return board[i][0]

        # Check vertically
        if (board[0][i] == board[1][i] == board[2][i]) and board[0][i] != EMPTY:
            return board[0][i]

    # Check diagonally
    if ((board[0][0] == board[1][1] == board[2][2]) or (board[0][2] == board[1][1] == board[2][0])) and board[1][1] != EMPTY:
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True

    numpyBoard = np.array(board)
    emptyCount = np.count_nonzero(numpyBoard == EMPTY)
    if emptyCount == 0:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winnerPlayer = winner(board)
    if winnerPlayer == X:
        return 1

    if winnerPlayer == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    currentPlayer = player(board)
    # X tries to maximize score (MAX(X))
    # O tries to minimize score (MIN(O))
    if currentPlayer == X:
        return max_value(board)[1]
    else:
        return min_value(board)[1]


def max_value(board):
    if terminal(board):
        return (utility(board), None)

    value = -sys.maxsize-1
    optimalAction = None
    for action in actions(board):
        possibleResult = min_value(result(board, action))
        if (possibleResult[0] > value):
            value = possibleResult[0]
            optimalAction = action

    return (value, optimalAction)


def min_value(board):
    if terminal(board):
        return (utility(board), None)

    value = sys.maxsize
    optimalAction = None
    for action in actions(board):
        possibleResult = max_value(result(board, action))
        if (possibleResult[0] < value):
            value = possibleResult[0]
            optimalAction = action

    return (value, optimalAction)
