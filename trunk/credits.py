# -*- coding: cp1252 -*-
import sys, pygame
from pygame.locals import *

class credits():
    def __init__(self, font, size):
        self.font = font
        self.width = size[0]
        self.height= size[1]
        self.rendered = []
        self.poses = []
        self.howtos = ("                          Credits"
                       , ""
                       , "      Programming           Paul D. Faria"
                       , "                                        rEtSaMfF"
                       , ""
                       , "      Art                             DaHornNPT"
                       , ""
                       , "      Sound                        Nintendo®"
                       , ""
                       , "Press [Enter] to return to the main menu")
        for string in range(0,len(self.howtos)):
            self.rendered.append(self.font.render(self.howtos[string], 1, (255, 255, 255)))
        for num in range(0, len(self.howtos)):
            self.poses.append((self.width / 2 - 240, self.height / 2 - (-num * 25) - 140))
        self.pointloc = 0
        self.pointpos = [self.width / 2 - 80, self.poses[self.pointloc][1] + 5]

def show_credits(font, screen, size, background):
    crdts = credits(font, size)
    screen.blit(background, (0, 0))
    for item, pos in zip(crdts.rendered, crdts.poses):
        screen.blit(item, pos)
    pygame.display.flip()
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return
                
    
