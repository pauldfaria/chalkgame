import pygame
from player import *

Fire = 3
Jump = 4
#MS = 4

class Human(Player):
    
    def __init__(self, animations, fireball, screen = (1024, 768)):
        Player.__init__(self, animations, screen)
        self.fireanim = self.animations[Fire][0]
        self.fireframes = self.animations[Fire][1]
        self.firetime = 0
        self.fireball = fireball
        self.jumpanim = self.animations[Jump][0]
        self.jumpframes = self.animations[Jump][1]
        self.jumptime = 0
        self.jumping = False
        self.kills = 0
        """self.msanim = self.animations[MS]
        self.mstime = 0
        self.msing = False
        self.unmsing = False"""
    
    def attack(self):
        self.animation.reset()
        Player.attack(self)
    
    def move(self, key):
        self.animation.reset()
        Player.move(self)
        if key == K_RIGHT:
            self.speed[0] = 6
        elif key == K_LEFT:
            self.speed[0] = -6
        elif key == K_UP:
            self.speed[1] = -6
        elif key == K_DOWN:
            self.speed[1] = 6
    
    def fire(self):
        self.mana -= 20
        self.curanim = self.fireanim
        self.frames = self.fireframes
        self.animate = True
        self.end = True
    
    def magic_shield(self):
        """will redefine when we have an animation for it"""
        pass
    
    def jump(self):
        self.curanim = self.jumpanim
        self.frames = self.jumpframes
        self.animate = True
        self.end = True
    
    def refresh(self):
        """temp = self.pos.move(self.speed)
        if temp.right > self.screen[0]:
            self.pos.right = self.screen[0]
            self.speed[0] = 0
        elif temp.left < 0:
            self.pos.left = 0
            self.speed[0] = 0
        elif temp.top < ((self.screen[1] ) / 2):
            self.pos.top = (self.screen[1] ) / 2
            self.speed[1] = 0
        elif temp.bottom > self.screen[1]:
            self.pos.bottom = self.screen[1]
            self.speed[1] = 0
        else:
            self.pos = temp"""
        Player.refresh(self)
    