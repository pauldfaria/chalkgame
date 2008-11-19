import sys, pygame
from pygame.locals import *

from level1 import *
from level2 import *
from level3 import *
from instructions import *
from credits import *

pygame.init()
font = pygame.font.Font(None, 36)

size = width, height = 1024, 768
screen = pygame.display.set_mode(size)

background = pygame.image.load('images/background.bmp').convert_alpha()

class menu():
    def __init__(self):
        self.values = ("Start", "Instructions", "Credits", "Quit")
        self.start = font.render(self.values[0], 1, (255, 255, 255))
        self.howto = font.render(self.values[1], 1, (0, 0, 0))
        self.credits = font.render(self.values[2], 1, (0, 0, 0))
        self.quit = font.render(self.values[3], 1, (0, 0, 0))
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
            self.items[self.pointloc] = font.render(self.values[self.pointloc]
                                                    , 1, (0, 0, 0))
            self.pointloc = len(self.items) - 1
            self.pointpos = [width / 2 - 80, self.poses[self.pointloc][1] + 5]
            self.items[self.pointloc] = font.render(self.values[self.pointloc]
                                                    , 1, (255, 255, 255))
            
        else:
            self.items[self.pointloc] = font.render(self.values[self.pointloc]
                                                    , 1, (0, 0, 0))
            self.pointloc -= 1
            self.pointpos = [width / 2 - 80, self.poses[self.pointloc][1] + 5]
            self.items[self.pointloc] = font.render(self.values[self.pointloc]
                                                    , 1, (255, 255, 255))
            
    
    def down(self):
        if self.pointloc == len(self.items) - 1:
            self.items[self.pointloc] = font.render(self.values[self.pointloc]
                                                    , 1, (0, 0, 0))
            self.pointloc = 0
            self.pointpos = [width / 2 - 80, self.poses[self.pointloc][1] + 5]
            self.items[self.pointloc] = font.render(self.values[self.pointloc]
                                                    , 1, (255, 255, 255))
        else:
            self.items[self.pointloc] = font.render(self.values[self.pointloc]
                                                    , 1, (0, 0, 0))
            self.pointloc += 1
            self.pointpos = [width / 2 - 80, self.poses[self.pointloc][1] + 5]
            self.items[self.pointloc] = font.render(self.values[self.pointloc]
                                                    , 1, (255, 255, 255))
    
    def execute(self):
        if self.pointloc == 0:
            if level1(size, screen):
                if level2(size, screen):
                    if level3(size, screen):
                        show_credits(font, screen, size, background)
        elif self.pointloc == 1:
            show_howto(font, screen, size, background)
        elif self.pointloc == 2:
            show_credits(font, screen, size, background)
        elif self.pointloc == 3:
            sys.exit()

def start_game():
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
                elif event.key == K_RETURN:
                    game.execute()
        
        screen.blit(background, (0, 0))
        for item, pos in zip(game.items, game.poses):
            screen.blit(item, pos)
        screen.blit(game.pointer, game.pointpos)
    
        pygame.display.flip()
        pygame.time.delay(100)
