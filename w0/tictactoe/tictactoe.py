"""
Tic Tac Toe Player
"""

import re
import copy

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
    # count filled fields (i.e., moves made)
    move_count = count_moves(board)
    # assumes X always makes the first move
    return X if move_count % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return None

    # determine empty fields
    actions = set()
    for row in range(3):
        for cell in range(3):
            if board[row][cell] == None:
                actions.add((row, cell))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    p = player(board) # determind current player
    new_b = copy.deepcopy(board)
    new_b[action[0]][action[1]] = p
    return new_b


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # get stringified version of board
    board_str = ''
    for row in board:
        for cell in row:
            board_str += cell if cell else ' '

    # call memoized function
    return find_winner(board_str)


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return True if winner(board) or count_moves(board) == 9 else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0


# an article that helped me understand the minimax algorithm: https://www.cosy.sbg.ac.at/~held/teaching/wiss_arbeiten/slides_19-20/KI_in_Videospielen.pdf
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # determine which player is the ai
    ai_p = player(board)

    # function to determine the max score of an action of the ai player
    def get_score(maximize, b):
        # if the game's over, return the utility for the ai player
        if terminal(b):
            u = utility(b) # returns utility for X (1, 0, or -1)
            return u if ai_p == X else -u # returns utility for ai player

        # get max score
        scores = set()
        for a in actions(b):
            # alpha-beta pruning
            if maximize:
                if 1 in scores: 
                    break
            else:
                if -1 in scores:
                    break
            # get result of next action and add scores recursively
            r = result(b, a)
            scores.add(get_score(not maximize, r))

        # return max() if maximize player, else min() of scores
        return max(scores) if maximize else min(scores)

    optimal_action = None
    optimal_score = -2

    for a in actions(board):
        r = result(board, a)
        score = get_score(False, r)
        if score > optimal_score:
            optimal_score = score
            optimal_action = a

    return optimal_action


# helpers
class Memoize:
    # source of this class: https://python-course.eu/advanced-python/memoization-decorators.php
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}
    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.fn(*args)
        return self.memo[args]


@Memoize # find_winner() is called often (by winner()), and it's not a cheap function
def find_winner(board_str):
    # pattern match to find winner
    ## winning patterns
    win = [
        '^t{3}', # 1st row
        '^.{3}t{3}', # 2nd row
        '^.{6}t{3}', # 3rd row
        '^(t{1}.{2}){3}', # 1st column
        '^(.{1}t{1}.{1}){3}', # 2nd column
        '^(.{2}t{1}){3}', # 3rd column
        '^(t{1}.{3}){2}t{1}', # diagonal left to right
        '^.{2}(t{1}.{1}){3}.{1}', # diagonal right to left
    ]
    ## prepare str for X and O win searches (t represents the respective player)
    str_x = board_str.replace('X', 't')
    str_o = board_str.replace('O', 't')
    ## find winner and return letter or None
    if any(re.search(w, str_x) for w in win):
        return X
    elif any(re.search(w, str_o) for w in win):
        return O
    else:
        return None


def count_moves(board):
    move_count = 0
    for row in board:
        for cell in row:
            if cell:
                move_count += 1
    return move_count