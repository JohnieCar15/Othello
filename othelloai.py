#!/usr/bin/env python3

import math
import copy
import random
import numpy as np
from collections import defaultdict

heuristic = [
[100, -10, 11, 6, 6, 11, -10, 100],
[-10, -20, 1, 2, 2, 1, -20, -10],
[10, 1, 5, 4, 4, 5, 1, 10],
[6, 2, 4, 2, 2, 4, 2, 6],
[6, 2, 4, 2, 2, 4, 2, 6],
[10, 1, 5, 4, 4, 5, 1, 10],
[-10, -20, 1, 2, 2, 1, -20, -10],
[100, -10, 11, 6, 6, 11, -10, 100]
]

def alphabeta(board, depth, alpha, beta, maximisingplayer):
    if depth == 0 or len(get_possible_moves(board, "B")) == 0:
        return (-1, -1), get_modified_score(board)["B"]
    
    if maximisingplayer:
        value = -math.inf
        moves = get_possible_moves(board, "B")
        if len(moves) != 0:
            best_move = random.choice(moves)
        else:
            return
        for move in moves:
            newboard = copy.deepcopy(board)
            newboard[move[1]][move[0]] = "B"
            new_score = alphabeta(newboard, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_move = move

            alpha = max(alpha, value)
            if value >= beta:
                break
        return best_move, value
    else:
        value = math.inf
        moves = get_possible_moves(board, "W")
        if len(moves) != 0:
            best_move = random.choice(moves)
        else:
            return
        for move in moves:
            newboard = copy.deepcopy(board)
            newboard[move[1]][move[0]] = "W"
            new_score = alphabeta(newboard, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_move = move
            beta = min(beta, value)
            if value <= alpha:
                break
        return best_move, value


class MonteCarloTreeSearchNode():
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return
    
    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions
    
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node 

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self):
        current_rollout_state = self.state
        
        while not current_rollout_state.is_game_over():
            
            possible_moves = current_rollout_state.get_legal_actions()
            
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
        
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
    
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):

        current_node = self
        while not current_node.is_terminal_node():
            
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100
        for i in range(simulation_no):
            
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        
        return self.best_child(c_param=0.)

    def get_legal_actions(self): 
        '''
        Modify according to your game or
        needs. Constructs a list of all
        possible actions from current state.
        Returns a list.
        '''
        return get_possible_moves(self.state)

    def is_game_over(self):
        '''
        Modify according to your game or 
        needs. It is the game over condition
        and depends on your game. Returns
        true or false
        '''
        return is_finished(self.state)

    def game_result(self):
        '''
        Modify according to your game or 
        needs. Returns 1 or 0 or -1 depending
        on your state corresponding to win,
        tie or a loss.
        '''

        total_scores = get_score(self.state)
        if total_scores["B"] > total_scores["W"]:
            return 1
        elif total_scores["W"] > total_scores["B"]:
            return -1
        else:
            return 0

    def move(self,action):
        '''
        Modify according to your game or 
        needs. Changes the state of your 
        board with a new value. For a normal
        Tic Tac Toe game, it can be a 3 by 3
        array with all the elements of array
        being 0 initially. 0 means the board 
        position is empty. If you place x in
        row 2 column 3, then it would be some 
        thing like board[2][3] = 1, where 1
        represents that x is placed. Returns 
        the new state after making a move.
        '''

        flip_pieces(action[1], action[0], "B", self.state)
        self.state[action[1]][action[0]] = "B"
        
        return self.state

def is_finished(board):
    if len(get_possible_moves(board, "B")) == 0 and len(get_possible_moves(board, "W")) == 0:
        return True

    return False

def get_score(board):
    dictscores = {'B': 0, 'W': 0, 'N': 0}
    for x in range(0, 8):
        for y in range(0, 8):
            if board[x][y] == "W":
                dictscores['W'] += 1
            elif board[x][y] == "B":
                dictscores['B'] += 1
            else:
                dictscores['N'] += 1
    
    return dictscores

def get_modified_score(board):
    global heuristic
    dictscores = {'B': 0, 'W': 0, 'N': 0}
    for x in range(0, 8):
        for y in range(0, 8):
            if board[x][y] == "W":
                dictscores['W'] += heuristic[x][y]
            elif board[x][y] == "B":
                dictscores['B'] += heuristic[x][y]
            else:
                dictscores['N'] += heuristic[x][y]
    
    return dictscores

def get_possible_moves(board, to_move):
    moves= []
    for y in range(0, 8):
        for x in range(0, 8):
            up = y - 1
            down = y + 1
            left = x - 1
            right = x + 1

            can_flip = False

            if board[y][x] != None:
                continue

            # Vertically upwards direction
            while up != -1:
                if board[up][x] == None:
                    break
                elif board[up][x] != to_move:
                    can_flip = True

                if board[up][x] == to_move and can_flip == False:
                    break

                if board[up][x] == to_move and can_flip == True:
                    moves.append((y, x))
                    break
                up -= 1

            up = y - 1
            can_flip = False

            # Vertically downwards direction
            while down != 8:
                if board[down][x] == None:
                    break
                elif board[down][x] != to_move:
                    can_flip = True


                if board[down][x] == to_move and can_flip == False:
                    break

                if board[down][x] == to_move and can_flip == True:
                    moves.append((y, x))
                    break
                down += 1

            down = y + 1
            can_flip = False

            # Horizontally to the left direction
            while left != -1:
                if board[y][left] == None:
                    break
                elif board[y][left] != to_move:
                    can_flip = True

                if board[y][left] == to_move and can_flip == False:
                    break

                if board[y][left] == to_move and can_flip == True:
                    moves.append((y, x))
                    break
                left -= 1

            left = x - 1
            can_flip = False

            # Horizontally to the right direction
            while right != 8:
                if board[y][right] == None:
                    break
                elif board[y][right] != to_move:
                    can_flip = True

                if board[y][right] == to_move and can_flip == False:
                    break

                if board[y][right] == to_move and can_flip == True:
                    moves.append((y, x))
                    break
                right += 1
            
            right = x + 1
            can_flip = False

            # Diagonally to the top left direction
            while up != -1 and left != -1:
                if board[up][left] == None:
                    break
                elif board[up][left] != to_move:
                    can_flip = True

                if board[up][left] == to_move and can_flip == False:
                    break

                if board[up][left] == to_move and can_flip == True:
                    moves.append((y, x))
                    break
                up -= 1
                left -= 1
            
            up = y - 1
            left = x - 1
            can_flip = False

            # Diagonally to the top right direction
            while up != -1 and right != 8:
                if board[up][right] == None:
                    break
                elif board[up][right] != to_move:
                    can_flip = True

                if board[up][right] == to_move and can_flip == False:
                    break

                if board[up][right] == to_move and can_flip == True:
                    moves.append((y, x))
                    break
                up -= 1
                right += 1
            
            right = x + 1

            can_flip = False

            # Diagonally to the bottom right direction
            while down != 8 and right != 8:
                if board[down][right] == None:
                    break
                elif board[down][right] != to_move:
                    can_flip = True


                if board[down][right] == to_move and can_flip == False:
                    break

                if board[down][right] == to_move and can_flip == True:
                    moves.append((y, x))
                    break
                down += 1
                right += 1
            
            down = y + 1

            can_flip = False

            # Diagonally to the bottom left direction
            while down != 8 and left != -1:
                if board[down][left] == None:
                    break
                elif board[down][left] != to_move:
                    can_flip = True

                if board[down][left] == to_move and can_flip == False:
                    break

                if board[down][left] == to_move and can_flip == True:
                    moves.append((y, x))
                    break
                down += 1
                left -= 1
    
    return moves

def flip_pieces(y_pos, x_pos, to_move, board):

    up = y_pos - 1
    down = y_pos + 1
    left = x_pos - 1
    right = x_pos + 1

    is_legal = False

    can_flip = False

    # Vertically upwards direction
    while up != -1:
        if board[up][x_pos] == None:
            break
        elif board[up][x_pos] != to_move:
            can_flip = True

        if board[up][x_pos] == to_move and can_flip == False:
            break

        if board[up][x_pos] == to_move and can_flip == True:
            is_legal = True
            for x in range(up, y_pos):
                board[x][x_pos] = to_move
            break
        up -= 1

    up = y_pos - 1
    can_flip = False

    # Vertically downwards direction
    while down != 8:
        if board[down][x_pos] == None:
            break
        elif board[down][x_pos] != to_move:
            can_flip = True


        if board[down][x_pos] == to_move and can_flip == False:
            break

        if board[down][x_pos] == to_move and can_flip == True:
            is_legal = True
            for x in range(y_pos, down):
                board[x][x_pos] = to_move
            break
        down += 1

    down = y_pos + 1
    can_flip = False

    # Horizontally to the left direction
    while left != -1:
        if board[y_pos][left] == None:
            break
        elif board[y_pos][left] != to_move:
            can_flip = True

        if board[y_pos][left] == to_move and can_flip == False:
            break

        if board[y_pos][left] == to_move and can_flip == True:
            is_legal = True
            for x in range(left, x_pos):
                board[y_pos][x] = to_move
            break
        left -= 1

    left = x_pos - 1
    can_flip = False

    # Horizontally to the right direction
    while right != 8:
        if board[y_pos][right] == None:
            break
        elif board[y_pos][right] != to_move:
            can_flip = True

        if board[y_pos][right] == to_move and can_flip == False:
            break

        if board[y_pos][right] == to_move and can_flip == True:
            is_legal = True
            for x in range(x_pos, right):
                board[y_pos][x] = to_move
            break
        right += 1
    
    right = x_pos + 1
    can_flip = False

    # Diagonally to the top left direction
    while up != -1 and left != -1:
        if board[up][left] == None:
            break
        elif board[up][left] != to_move:
            can_flip = True

        if board[up][left] == to_move and can_flip == False:
            break

        if board[up][left] == to_move and can_flip == True:
            is_legal = True
            for x in range(up, y_pos):
                board[x][left] = to_move
                left += 1
            break
        up -= 1
        left -= 1
    
    up = y_pos - 1
    left = x_pos - 1
    can_flip = False

    # Diagonally to the top right direction
    while up != -1 and right != 8:
        if board[up][right] == None:
            break
        elif board[up][right] != to_move:
            can_flip = True

        if board[up][right] == to_move and can_flip == False:
            break

        if board[up][right] == to_move and can_flip == True:
            is_legal = True
            for x in range(up, y_pos):
                board[x][right] = to_move
                right -= 1
            break
        up -= 1
        right += 1
    
    right = x_pos + 1

    can_flip = False

    # Diagonally to the bottom right direction
    while down != 8 and right != 8:
        if board[down][right] == None:
            break
        elif board[down][right] != to_move:
            can_flip = True


        if board[down][right] == to_move and can_flip == False:
            break

        if board[down][right] == to_move and can_flip == True:
            is_legal = True
            for x in range(down, y_pos, -1):
                board[x][right] = to_move
                right -= 1
            break
        down += 1
        right += 1
    
    down = y_pos + 1

    can_flip = False

    # Diagonally to the bottom left direction
    while down != 8 and left != -1:
        if board[down][left] == None:
            break
        elif board[down][left] != to_move:
            can_flip = True

        if board[down][left] == to_move and can_flip == False:
            break

        if board[down][left] == to_move and can_flip == True:
            is_legal = True
            for x in range(down, y_pos, -1):
                board[x][left] = to_move
                left += 1
            break
        down += 1
        left -= 1
    
    return is_legal