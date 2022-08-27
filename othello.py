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

def drawGrid():
    for x in range(0, WIDTH, WIDTH // 8):
        for y in range(0, HEIGHT, HEIGHT // 8):
            rect = pygame.Rect(x, y, WIDTH / 8, HEIGHT / 8)
            pygame.draw.rect(SCREEN, WHITE, rect, 5)

while True:
    drawGrid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()