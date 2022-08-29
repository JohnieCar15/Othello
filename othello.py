#!/usr/bin/env python3

import pygame, sys
import math
 
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

def flip_pieces(y_pos, x_pos, to_move):
    global board
    up = y_pos - 1
    down = y_pos + 1
    left = x_pos - 1
    right = x_pos + 1

    # Vertically upwards direction
    while up != -1:
        if board[up][x_pos] == to_move:
            for x in range(up, y_pos):
                board[x][x_pos] = to_move
        up -= 1

    up = y_pos - 1

    # Vertically downwards direction
    while down != 8:
        if board[down][x_pos] == to_move:
            for x in range(y_pos, down):
                board[x][x_pos] = to_move
        down += 1

    down = y_pos + 1

    # Horizontally to the left direction
    while left != -1:
        if board[y_pos][left] == to_move:
            for x in range(left, x_pos):
                board[y_pos][x] = to_move
        left -= 1

    left = x_pos - 1

    # Horizontally to the right direction
    while right != 8:
        if board[y_pos][right] == to_move:
            for x in range(x_pos, right):
                board[y_pos][x] = to_move
        right += 1
    
    right = x_pos + 1

    # Diagonally to the top left direction
    while up != -1 and left != -1:
        if board[up][left] == to_move:
            for x in range(up, y_pos):
                board[x][left] = to_move
                left += 1
        up -= 1
        left -= 1
    
    up = y_pos - 1
    left = x_pos - 1

    # Diagonally to the top right direction
    while up != -1 and right != 8:
        if board[up][right] == to_move:
            for x in range(up, y_pos):
                board[x][right] = to_move
                right -= 1
        up -= 1
        right += 1
    
    right = x_pos + 1

    # Diagonally to the bottom right direction
    while down != 8 and right != 8:
        if board[down][right] == to_move:
            for x in range(y_pos, down):
                board[x][right] = to_move
                right -= 1
        down += 1
        right += 1
    
    down = y_pos + 1

    # Diagonally to the bottom left direction
    while down != 8 and left != -1:
        if board[down][left] == to_move:
            for x in range(y_pos, down):
                board[x][left] = to_move
                left += 1
        down += 1
        left -= 1
    

def adjust_board(to_move):
    global board
    coordinates = pygame.mouse.get_pos()
    x_pos = math.floor(coordinates[0] / (WIDTH / 8))
    y_pos = math.floor(coordinates[1] / (HEIGHT / 8))

    if board[y_pos][x_pos] == None:
        board[y_pos][x_pos] = to_move
        flip_pieces(y_pos, x_pos, to_move)
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
            to_move = adjust_board(to_move)

    pygame.display.update()