import pygame
import numpy as np

pygame.init() 

BLACK = (0, 0, 0)
RED = (250, 0, 0)   
WHITE = (255, 255, 255)

# make a 2d array
height = 4
width = 4
SIZE = 50
grid = np.zeros((width, height))

screenSize = [width*SIZE, height*SIZE]  

screen = pygame.display.set_mode(screenSize) 

done = False 

def drawRect(x, y, colour):
    # ^^ draw Rectangle
    pygame.draw.rect(screen, colour, (x*SIZE+1, y*SIZE+1, SIZE-2, SIZE-2))
    # ^^ (x*SIZE+1) & (y*SIZE+1) gets it where it is meant to be

grid[2, 2] = 0 #for example: setting this to 1 will make this specific coordinate into a black square, can do this for any.

currentX = 1
currentY= 1


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                currentX -= 1
                # ^^same as: "currentX = currentX-1"
            elif event.key == pygame.K_RIGHT:
                currentX += 1
            elif event.key == pygame.K_UP:
                currentY -= 1
            elif event.key == pygame.K_DOWN:
                currentY += 1

                # going down is taking an up away therefore -1 for going up
    
    grid[currentX, currentY] = 1

    screen.fill(WHITE)

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x, y] == 0:
                drawRect(x, y, RED)
            elif grid[x, y] == 1:
                drawRect(x, y, BLACK)
 
    pygame.display.flip() 
  
    grid[currentX, currentY] = 0