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
    
    def fire(self):
        self.curanim = self.fireanim
        self.curframes = self.fireframes
        self.animate = True
        self.end = True
    
    def magic_shield(self):
        """will redefine when we have an animation for it"""
    
    def jump(self):
        self.curanim = self.jumpanim
        self.curframes = self.jumpframes
        self.animate = True
        self.end = True
    