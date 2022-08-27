#!/usr/bin/env python3

import pygame, sys
import math
 
pygame.init()

WIDTH, HEIGHT = 900, 900

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE|pygame.DOUBLEBUF|pygame.HWSURFACE)
pygame.display.set_caption("Othello")

BOARD = pygame.image.load("othelloassets/Board.png")

SCREEN.blit(pygame.transform.scale(BOARD, (WIDTH, HEIGHT)), (0, 0))
pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()