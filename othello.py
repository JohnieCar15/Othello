#!/usr/bin/env python3

import pygame, sys
import math

from othelloai import get_score, get_possible_moves, alphabeta, is_finished, flip_pieces, MonteCarloTreeSearchNode
 
pygame.init()

WIDTH, HEIGHT = 900, 900
GREEN = (64, 83, 54)
WHITE = (200, 200, 200)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE|pygame.DOUBLEBUF|pygame.HWSURFACE)
pygame.display.set_caption("Othello")

SCREEN.fill(GREEN)

to_move = "B"

board = [[None, None, None, None, None, None, None, None], 
[None, None, None, None, None, None, None, None],
[None, None, None, None, None, None, None, None],
[None, None, None, "W", "B", None, None, None],
[None, None, None, "B", "W", None, None, None],
[None, None, None, None, None, None, None, None],
[None, None, None, None, None, None, None, None],
[None, None, None, None, None, None, None, None]]

def render_board():
    global board
    for x in range(0, 8):
        for y in range(0, 8):
            if board[x][y] != None:
                color = (200, 200, 200) if board[x][y] == "W" else (0, 0, 0)
                pygame.draw.circle(SCREEN, color, (y * (HEIGHT / 8) + HEIGHT / 16, x * (WIDTH / 8) + WIDTH / 16), 30)  


def adjust_board(to_move):
    global board
    coordinates = pygame.mouse.get_pos()
    x_pos = math.floor(coordinates[0] / (WIDTH / 8))
    y_pos = math.floor(coordinates[1] / (HEIGHT / 8))

    # Considers case where player is unable to make move but opponent has remaining moves
    other_player = "W" if to_move == "B" else "B"
    if len(get_possible_moves(board, to_move)) == 0:
        if len(get_possible_moves(board, other_player)) != 0:
            to_move = other_player 
            return

    if board[y_pos][x_pos] == None:
        if not flip_pieces(y_pos, x_pos, to_move, board):
            return to_move
        board[y_pos][x_pos] = to_move
        
        to_move = "B" if to_move == "W" else "W"

    render_board()
    
    return to_move


def drawGrid():
    for x in range(0, WIDTH, WIDTH // 8):
        for y in range(0, HEIGHT, HEIGHT // 8):
            rect = pygame.Rect(x, y, WIDTH / 8, HEIGHT / 8)
            pygame.draw.rect(SCREEN, WHITE, rect, 5) 

while True:
    drawGrid()
    render_board()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if to_move == "B":
                # coordinates = alphabeta(board, 5, -math.inf, math.inf, True)[0]
                # flip_pieces(coordinates[0], coordinates[1], to_move, board)
                # board[coordinates[0]][coordinates[1]] = "B"
                root = MonteCarloTreeSearchNode(state = board)
                selected_node = root.best_action()
                print(selected_node)
                render_board()
                to_move = "W"
            else:
                to_move = adjust_board(to_move)
            
            if is_finished(board):
                print("Game finished!")
                print(get_score(board))
                sys.exit()
            

    pygame.display.update()