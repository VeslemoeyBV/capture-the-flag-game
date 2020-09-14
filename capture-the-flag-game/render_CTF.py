
import pygame
import numpy as np

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
L_YELLOW = (247, 250, 185)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (193, 230, 62)
M_GREEN = (177, 184, 35) #murky green


def drawplayer(colour, direction, position, win):
    #r = row
    #c = column
    r = position[0]
    c = position[1]
    pygame.draw.circle(win, colour, (r*21+10, c*21+10), 10)
    if direction == 1:
        pygame.draw.circle(win, BLACK, (r*21+10, c*21+2), 3)
    if direction == 2:
        pygame.draw.circle(win, BLACK, (r*21+10, c*21+18), 3)
    if direction == 3:
        pygame.draw.circle(win, BLACK, (r*21+2, c*21+10), 3)
    if direction == 4:
        pygame.draw.circle(win, BLACK, (r*21+18, c*21+10), 3)


def render(array):
    WINSIZE = (array.shape[0]*21, array.shape[1]*21)
    win = pygame.display.set_mode(WINSIZE)
    win.fill(M_GREEN)
    for r, row in enumerate(array):
        for c, cell in enumerate(row):
            if cell == 18:
                pygame.draw.rect(win, L_YELLOW, (r*21, c*21, 20, 20))
            if cell == 0:
                pygame.draw.rect(win, WHITE, (r*21, c*21, 20, 20))
            if cell > 0 and cell < 5:
                pygame.draw.rect(win, L_YELLOW, (r*21, c*21, 20, 20))
                drawplayer(BLUE, cell, (r, c), win)
            if cell > 4 and cell < 9:
                pygame.draw.rect(win, L_YELLOW, (r*21, c*21, 20, 20))
                drawplayer(RED, cell-4, (r, c), win)
            if cell == 9:
                pygame.draw.rect(win, L_YELLOW, (r*21, c*21, 20, 20))
                pygame.draw.circle(win, GREEN, (r*21+10, c*21+10), 10)
            if cell > 9 and cell < 14:
                pygame.draw.rect(win, L_YELLOW, (r*21, c*21, 20, 20))
                drawplayer(BLUE, cell-9, (r, c), win)
                pygame.draw.circle(win, GREEN, (r*21+17, c*21+10), 3)
            if cell > 13 and cell < 18:
                pygame.draw.rect(win, L_YELLOW, (r*21, c*21, 20, 20))
                drawplayer(RED, cell-13, (r, c), win)
                pygame.draw.circle(win, GREEN, (r*21+17, c*21+10), 3)
    
    pygame.win.flip()

