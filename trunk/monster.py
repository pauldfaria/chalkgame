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
    
    def refresh(self):
        # I realized here, that all monsters need to know
        # where the players are, but we don't have that =p
        # pass

        # I added back some of the same code from the player class because
        # we don't want the monsters to be going off the screen - Calvin
        # also, now the box dies when it goes off the left and can be respawned
        
        self.pos.right += self.speed[0]
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
        return True
