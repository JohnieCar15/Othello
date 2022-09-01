#!/usr/bin/env python3

import math
import copy

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

moves = []

def alphabeta(board, depth, alpha, beta, maximisingplayer):
    global moves
    if depth == 0 or len(get_possible_moves(board, "B")) == 0:
        return (-1, -1), get_modified_score(board)["B"]
    
    if maximisingplayer:
        value = -math.inf
        for move in get_possible_moves(board, "B"):
            newboard = copy.deepcopy(board)
            newboard[move[1]][move[0]] = "B"
            new_score = alphabeta(newboard, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_move = move

            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_move, value
    else:
        value = math.inf
        for move in get_possible_moves(board, "W"):
            newboard = copy.deepcopy(board)
            newboard[move[1]][move[0]] = "W"
            new_score = alphabeta(newboard, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break
        return best_move, value

def print_moves():
    global moves
    print(moves)


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

