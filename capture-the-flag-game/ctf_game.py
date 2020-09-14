import numpy as np

GRIDSIZE = (16, 11)
VISION = 3
grid = np.zeros(GRIDSIZE)
grid[3, 2] = 1

def seen(row, column, players):
    seen = False
    for player in players:

        if player.dir == 3:  #is LEFT
            if player.x < column and abs (player.y-row)<=VISION//2:
                seen = True

        if player.dir == 1: 
            if player.y < column and abs (player.x-column)<=VISION//2:
                seen = True

        if player.dir == 2:
            if player.x > column and abs (player.y-row)<=VISION//2:
                seen = True

        if player.dir == 0:
            if player.y > column and abs (player.x-column)<=VISION//2:
                seen = True
        
        if(player.x, player.y) == (column, row):
            seen = True

    return seen

#abs is absolute value, so if negative become positive (same as modulus)



class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.starting_x = x
        self.starting_y = y
        self.dir = 3
        self.stunned = 0
        #where dir represents direction
    
    def reset(self, grid):
        grid[self.x, self.y] = 0
        self.x = self.starting_x
        self.y = self.starting_y
        self.dir = 3
        grid[self.x, self.y] = 1
        return grid 

        #grid[self.x, self.y] = 0
        #self.x = self.starting_x
        #self.y = self.starting_y
        #self.dir = 3
        #grid[self.x, self.y] = 1
        #return grid

    def step(self, grid, move):
        #the movement function
        #where move is the movement made
        #DOWN (0), UP (1), LEFT (2), RIGHT (3)

        if self.stunned == 0:
            ox = self.x
            oy = self.y

            #where ox, oy is original x, original y

            grid[ox, oy] = 0
            if move == 0:
                self.dir = 0
                self.y = min(max(0, self.y-1), GRIDSIZE[1]-1)
            elif move == 1:
                self.dir = 1
                self.y = min(max(0, self.y+1), GRIDSIZE[1]-1)
            elif move == 2:
                self.dir = 2
                self.x = min(max(0, self.x-1), GRIDSIZE [0]-1)
            elif move == 3:
                self.dir = 3
                self.x = min(max(0, self.x+1), GRIDSIZE [0]-1)

            if grid[self.x, self.y] !=0:        #if it is not equal to zero
                self.x = ox
                self.y = oy
                grid[self.x, self.y] = 1
        else:
            self.stunned -= 1
        return grid


class Team():
    def __init__(self):
        self.P1 = Player(3, GRIDSIZE[1]//2)  #GRIDSIZE[1]//2 represents center
        self.P2 = Player(5, GRIDSIZE[1]//2)
        self.flagx = GRIDSIZE[0]-1      #(minus one because python indexiing starts at 0)
        self.flagy = GRIDSIZE[1]//2
        self.flag_bound = 0             #who is connected (bound)to the flag

    def reset(self, grid):
        grid = self.P1.reset(grid)
        grid = self.P2.reset(grid)
        np.remainder(grid, 2, out=grid)
        grid[self.flagx, self.flagy] = 0
        self.flagx = GRIDSIZE[0]-1
        self.flagy = GRIDSIZE[1]//2
        grid[self.flagx, self.flagy] = 1
        return grid

    def step(self, grid, m1, m2): 
        # where m1 is p1's move, m2 is p2's move
        grid = self.P1.step(grid, m1)
        grid = self.P2.step(grid, m2)

        np.remainder(grid, 2, out=grid)

        if self.flag_bound == 1:
            self.flagx = self.P1.x
            self.flagy = self.P1.y
        if self.flag_bound == 2:
            self.flagx = self.P2.x
            self.flagy = self.P2.y

        if (self.P1.x, self.P1.y) == (self.flagx, self.flagy):
            self.flag_bound = 1
        if (self.P2.x, self.P2.y) == (self.flagx, self.flagy):
            self.flag_bound = 2

        if self.flag_bound == 0:
            grid = self.protectFlag(0)

        return self.protectFlag(grid)
#render seperately because the enemy is always on the right and so the teams see different things,
#players on other team see other things so two pictures end up being different

    def render(self, oflagx, oflagy, op1, op2):
        #op1 and op2 are opponent player
        #oflagx and oflagy are opponent flags

        #0 will be the - see nothing there
        #1-4 - a player is there (facing in a certain direction, there are four directions)
        #5-8 - an enemy player (facing certain direction)
        #9 there is a flag
        #10-17 any player and a flag
        #18 nothing is seen

        image = np.zeros(GRIDSIZE)
        image[self.P1.x, self.P1.y] = self.P1.dir+1
        image[self.P2.x, self.P2.y] = self.P2.dir+1

        dir_change = [0, 1, 3, 2]
        image[GRIDSIZE[0]-1-op1.x, op1.y] = dir_change[op1.dir]+5
        image[GRIDSIZE[0]-1-op2.x, op2.y] = dir_change[op2.dir]+5
        image[self.flagx, self.flagy] += 9
        image[oflagx, oflagy] += 9

        for row in range(GRIDSIZE[1]):
            for column in range(GRIDSIZE[0]):
                if not seen(row, column, [self.P1, self.P2]):
                    image[column, row] = 18

        return image

    def protectFlag(self, grid):
        xmin = max(0, self.flagx-1)
        xmax = min(GRIDSIZE[0],self.flagx+2)
        ymin = max(0, self.flagx-1)
        ymax = min(GRIDSIZE[1], self.flagy+2)
       
        grid[xmin:xmax, ymin:ymax] = 2
        return grid
        
class CTF():
    #capture the flag class
    def __init__(self):
        self.T1 = Team()
        self.T2 = Team()
        self.grid = np.zeros(GRIDSIZE)

    def reset (self):
        self.grid = self.T1.reset(grid)
        self.grid = np.flip(self.T2.reset(np.flip(self.grid, 0)))

    def step(self, t1p1, t1p2, t2p1, t2p2):
        #Move both teams
        #if one of the players are caught
        #reset the player
        #set stunned to 10 (a bigger number)
        
        #self.T1.step(t1p1, t1p2, grid)
        #np.flip(self.T2.step(np.flip(self.grid, 0), t2p1, t2p1, grid))

        p1 = 1
        for a in [self.T1.P1, self.T1.P2]:
            p2 =1
            for b in [self.T2.P1, self.T2.P2]:
                tx = GRIDSIZE[0]-1-b.x  #tx is the flipped version of b.x
                if abs(a.x-tx)+abs(a.y-b.y) < 2:
                    if a.x > (GRIDSIZE[0]-1)/2-1:
                        if self.T1.flag_bound == p1:
                            self.T1.flag_bound = 0        

                            self.T1.flagx -= a.x - tx
                            self.T1.flagy += a.y - b.y

                        self.grid=a.reset(self.grid)
                        a.stunned = 10

                    if b.x > (GRIDSIZE[0]-1)/2-1:
                        if self.T2.flag_bound == p2:
                            self.T2.flag_bound = 0        

                            self.T2.flagx -= a.x - tx
                            self.T2.flagy += a.y - b.y

                        self.grid= np.flip(b.reset(np.flip(self.grid, 0)), 0)
                        b.stunned = 10
                    p2 += 1
                p1 += 1

            self.grid = self.T1.step(self.grid, t1p1, t1p2)
            self.grid = np.flip(self.T2.step(np.flip(self.grid, 0), t2p1, t2p2), 0) #0 means x-axis gets flipped, if 1 then y axis would be flipped (would be useless)

    def render(self):
        image1 = self.T1.render(GRIDSIZE[0]-1-self.T2.flagx, self.T2.flagy, self.T2.P1, self.T2.P2)
        image2 = self.T1.render(GRIDSIZE[0]-1-self.T1.flagx, self.T1.flagy, self.T1.P1, self.T1.P2)
        return image1, image2

print(grid)








            
