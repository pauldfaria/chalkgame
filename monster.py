import pygame
from player import *

class Monster(Player):
    
    def __init__(self, animations, strength, screen = (1024, 768)):
        Player.__init__(self, animations, screen)
        self.strength = strength
    
    def move(self, speed):
        Player.move(self)
        self.speed = speed
    
    def refresh(self):
        # I realized here, that all monsters need to know
        # where the players are, but we don't have that =p
        # pass

        # I added back some of the same code from the player class because
        # we don't want the monsters to be going off the screen - Calvin
        # also, now the box dies when it goes off the left and can be respawned
        
        """self.pos.right += self.speed[0]
        self.pos.left += self.speed[0]
        self.pos.top += self.speed[1]
        self.pos.bottom += self.speed[1]
        if (self.pos.right > self.screen[0]):
            #self.pos.right = self.screen[0]
            self.speed[0] = 0
        elif (self.pos.left < 0):
            self.kill()
            return False
        elif (self.pos.top < (self.screen[1] * 5 / 8)):
            self.pos.top = (self.screen[1] * 5 / 8)
            self.speed[1] = 0
        elif (self.pos.bottom > self.screen[1]):
            self.pos.bottom = self.screen[1]
            self.speed[1] = 0
        return True"""
        Player.refresh(self)
