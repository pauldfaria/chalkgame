import pygame
from player import *

class Monster(Player):
    
    def __init__(self, animations, fireball, screen = (640, 480)):
        Player.__init__(self, animations)
        self.animations = animations
        self.old = self.animations[Normal]
        self.image = self.animations[Normal]
        self.defanim = self.animations[Defend]
        self.deftime = 0
        self.defending = False
        self.undefending = False
        self.atkanim = self.animations[Attack]
        self.atktime = 0
        self.attacking = False
        self.unattacking = False
        self.jumptime = 0
        self.jumping = False
        self.unjumping = False 
        self.fireanim = self.animations[Fire]
        self.firetime = 0
        self.fireball = fireball
        self.msanim = self.animations[MS]
        self.mstime = 0
        self.msing = False
        self.unmsing = False
        self.speed = [0, 0]
        self.pos = self.image.get_rect().move(0, screen[1])
        self.screen = screen
        self.special = False
        self.health = 100
        self.mana = 100
        self.whichanim = Normal
        self.counter = 0
