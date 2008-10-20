import pygame
from player import *

Defend = 2
Defmov = 3
Fire = 4
Jump = 5
#MS = 4

class Human(Player):
    
    def __init__(self, animations, fireball, strength, screen = (1024, 768)):
        Player.__init__(self, animations, screen)
        
        #defending variables
        self.defanim = self.animations[Defend][0]
        self.defframes = self.animations[Defend][1]
        self.defending = False
        
        #defending and moving at once variables
        self.defmovanim = self.animations[Defmov][0]
        self.defmovframes = self.animations[Defmov][1]
        self.moving = False
        
        #fire variables
        self.fireanim = self.animations[Fire][0]
        self.fireframes = self.animations[Fire][1]
        self.firerel = self.animations[Fire][2]
        self.special = False
        self.fireball = fireball
        self.firepos = self.pos
        
        #jumping variables
        self.jumpanim = self.animations[Jump][0]
        self.jumpframes = self.animations[Jump][1]
        self.jumping = False
        
        self.kills = 0
        self.strength = strength
        
        #only humans have mana
        self.mana = 100
        """self.msanim = self.animations[MS]
        self.msing = False
        self.unmsing = False"""
    
    def attack(self):
        self.animation.reset()
        self.special = False
        Player.attack(self)
    
    def defend(self):
        self.animation.reset()
        self.attacking = False
        self.defending = True
        self.special = False
        self.moving = False
        self.curanim = self.defanim
        self.frames = self.defframes
        self.animate = True
        self.end = False
    
    def defmov(self):
        self.animation.reset()
        self.attacking = False
        self.defending = True
        self.special = False
        self.curanim = self.defmovanim
        self.frames = self.defmovframes
        self.animate = True
        self.end = False
    
    def stop_defending(self):
        self.animation.reset()
        self.animate = False
        self.end = True
        self.curanim = self.movanim
        self.frames = self.movframes
        self.defending = False
    
    def walk(self, key):
        self.animation.reset()
        self.moving = True
        self.special = False
        self.defending = False
        Player.move(self)
        self.move(key)
    
    def move(self, key):
        if key == K_RIGHT:
            self.speed[0] = 6
        elif key == K_LEFT:
            self.speed[0] = -6
        elif key == K_UP:
            self.speed[1] = -6
        elif key == K_DOWN:
            self.speed[1] = 6
    
    def stop_ud(self):
        Player.stop_ud(self)
        if self.speed[0] == 0:
            self.moving = False
            if self.defending:
                self.defend()
    
    def stop_lr(self):
        Player.stop_lr(self)
        if self.speed[1] == 0:
            self.moving = False
            if self.defending:
                self.defend()
    
    def fire(self):
        self.mana -= 20
        self.moving = False
        self.special = True
        self.curanim = self.fireanim
        self.frames = self.fireframes
        self.animate = True
        self.end = True
    
    def getfirepos(self):
        self.firepos.top = self.pos.top + 90
        self.firepos.left = self.pos.left + 100
        return self.firepos
    
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
        if (self.mana < 100) and (self.counter % 50 == 0):
            self.mana += 1
        Player.refresh(self)
        if self.special and self.animation.cur_frame == self.firerel and self.counter % 5 == 0:
            return True
        if self.special and self.animation.cur_frame == self.fireframes - 1:
            self.special = False
        return False
