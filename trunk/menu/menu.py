import sys, pygame
from pygame.locals import *

pygame.init()

font = pygame.font.Font(None, 36)

size = width, height = 640, 480
screen = pygame.display.set_mode(size)
background = pygame.image.load('images/background.bmp').convert()

class menu():
    def __init__(self):
        self.start = font.render("Start", 1, (0, 0, 0))
        self.howto = font.render("Instructions", 1, (0, 0, 0))
        self.credits = font.render("Credits", 1, (0, 0, 0))
        self.quit = font.render("Quit", 1, (0, 0, 0))
        self.pointer = pygame.image.load("images/pointer.gif").convert()
        self.items = [self.start, self.howto, self.credits, self.quit]
        self.poses = [(width / 2 - 60, height / 2 - 40)
                    ,(width / 2 - 60, height / 2 - 20)
                    ,(width / 2 - 60, height / 2 )
                    ,(width / 2 - 60, height / 2 + 20)]
        self.pointloc = 0
        self.pointpos = [width / 2 - 80, self.poses[self.pointloc][1] + 5]
    
    def up(self):
        if self.pointloc == 0:
            pass
        else:
            self.pointloc -= 1
            self.pointpos = [width / 2 - 80, self.poses[self.pointloc][1] + 5]
    
    def down(self):
        if self.pointloc == 3:
            pass
        else:
            self.pointloc += 1
            self.pointpos = [width / 2 - 80, self.poses[self.pointloc][1] + 5]

game = menu()

while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_DOWN:
                game.down()
            elif event.key == K_UP:
                game.up()
        
    screen.blit(background, (0, 0))
    for item, pos in zip(game.items, game.poses):
        screen.blit(item, pos)
    screen.blit(game.pointer, game.pointpos)
    
    pygame.display.flip()
    pygame.time.delay(100)