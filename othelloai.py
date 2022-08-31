#!/usr/bin/env python3

import math
import copy

heuristic = [
[1000, -10, 10, 10, 10, 10, -10, 1000],
[-10, -10, 1, 1, 1, 1, -10, -10],
[10, 1, 1, 1, 1, 1, 1, 10],
[10, 1, 1, 1, 1, 1, 1, 10],
[10, 1, 1, 1, 1, 1, 1, 10],
[10, 1, 1, 1, 1, 1, 1, 10],
[-10, -10, 1, 1, 1, 1, -10, -10],
[1000, -10, 10, 10, 10, 10, -10, 1000]
]

def alphabeta(board, depth, alpha, beta, maximisingplayer):
    newboard = copy.deepcopy(board)
    if depth == 0 or len(get_possible_moves(newboard, maximisingplayer)) == 0:
        return [get_score(newboard)[maximisingplayer], []]
    
    if maximisingplayer == "B":
        value = [-math.inf, []]
        for move in get_possible_moves(newboard, maximisingplayer):
            newboard[move[0]][move[1]] = maximisingplayer
            value = value if value[0] > alphabeta(newboard, depth - 1, alpha, beta, "W")[0] else alphabeta(newboard, depth - 1, alpha, beta, "W")
            if value[0] >= beta:
                value[1].append(move)
                break
            alpha = max(alpha, value[0])
        return value
    else:
        value = [math.inf, (-1, -1)]
        for move in get_possible_moves(newboard, maximisingplayer):
            newboard[move[0]][move[1]] = maximisingplayer
            value = value if value[0] < alphabeta(newboard, depth - 1, alpha, beta, "B")[0] else alphabeta(newboard, depth - 1, alpha, beta, "B")
            if value[0] <= alpha:
                value[1].append(move) 
                break
            beta = min(beta, value[0])
        return value

def get_possible_moves(board, to_move):
    moves= []
    for x in range(0, 8):
        for y in range(0, 8):
            up = y - 1
            down = y + 1
            left = x - 1
            right = x + 1

            can_flip = False

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