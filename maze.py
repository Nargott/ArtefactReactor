from mazelib import Maze
from mazelib.generate.Prims import Prims

import pygame as py

screen_height = 880
screen_width = int(screen_height*1.0)

mx = 11; my = 11 # width and height of the maze
size = screen_height / mx

colors = [(0, 0, 0), (0, 200, 0), (255, 0, 0), (255, 255, 0)] # RGB colors of the maze

m = Maze()
m.generator = Prims(5, 5)
m.generate()
m.generate_entrances(True, True)
print(m.tostring(True)) 
m.grid[m.start[0]][m.start[1]] = 2
m.grid[m.end[0]][m.end[1]] = 3

py.init()

screen = py.display
screen_surf = screen.set_mode((screen_width,screen_height))

class Player(object):
    
    def __init__(self, pos):
        self.rect = py.Rect(pos[1]*size, pos[0]*size, size-1, size-1)
    def move(self, dx, dy):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = py.Rect(pos[0], pos[1], size-1, size-1)

player = Player(m.start)
walls = []

clock = py.time.Clock()

#for ky in range(my):
#    for kx in range(mx):
#        py.draw.rect(screen_surf, color[m.grid[kx][ky]], (ky*size, kx*size, size-1, size-1))

x = y = 0
for row in m.grid:
    for col in row:
        if col == 1:
            Wall((x, y))
        if col == 3:
            end_rect = py.Rect(x, y, size-1, size-1)
        x += size
    y += size
    x = 0


while True:
    clock.tick(20)
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            quit()
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                py.quit()
                quit()
                
    key = py.key.get_pressed()
    if key[py.K_LEFT]:
        player.move(-size, 0)
    if key[py.K_RIGHT]:
        player.move(size, 0)
    if key[py.K_UP]:
        player.move(0, -size)
    if key[py.K_DOWN]:
        player.move(0, size)
        
    if player.rect.colliderect(end_rect):
        py.quit()
        quit()
        
    screen_surf.fill((0, 0, 0))
    for wall in walls:
        py.draw.rect(screen_surf, colors[1], wall.rect)
    py.draw.rect(screen_surf, colors[3], end_rect)
    py.draw.rect(screen_surf, colors[2], player.rect)
    py.display.flip()