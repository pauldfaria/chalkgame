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
        #self.unjumping = False
        """self.msanim = self.animations[MS]
        self.mstime = 0
        self.msing = False
        self.unmsing = False"""
    
    def fire(self):#, firezorz):
        self.curanim = self.fireanim
        self.curframesd = self.fireframes
        self.animate = True
        self.end = True
        """if firezorz:
            self.special = True
            self.firing = True
            self.image = self.fireanim[self.firetime]
            self.firetime += 1
            pygame.time.set_timer(pygame.USEREVENT + 3, 90)
            if self.firetime == 3:
                fireball = Fireball(self.fireball, self.pos.move(10, 25) , self.screen[0])
                self.firing = False
                self.mana -= 20
                return fireball
        else:
            if self.firetime == 0:
                pygame.time.set_timer(pygame.USEREVENT + 3, 0)
                self.image = self.old
                self.special = False
            else:
                self.firetime -= 1
                self.image = self.fireanim[self.firetime]
                pygame.time.set_timer(pygame.USEREVENT + 3, 90)"""
    
    def magic_shield(self):#, magicorz):
        """if magicorz:
            self.special = True
            self.image = self.msanim[self.mstime]
            self.mstime += 1
            if self.mstime == 9:
                self.msing = True
                self.unmsing = True
                self.mana -= 45
                pygame.time.set_timer(pygame.USEREVENT + 4, 500)
            else:
                pygame.time.set_timer(pygame.USEREVENT + 4, 40)
        else:
            if self.mstime == 0:
                pygame.time.set_timer(pygame.USEREVENT + 4, 0)
                self.unmsing = False
                self.image = self.old
                self.special = False
            else:
                self.mstime -= 1
                self.image = self.msanim[self.mstime]
                pygame.time.set_timer(pygame.USEREVENT + 4, 40)"""
    
    def jump(self):#, jumporz):
        self.curanim = self.jumpanim
        self.curframes = self.jumpframes
        self.animate = True
        self.end = True
        """if jumporz:
            self.jumptime += 1
            pygame.time.set_timer(pygame.USEREVENT + 5, 40)
            if self.jumptime == 1:
                self.jumping = True
                self.speed[1] = -2
                pygame.time.set_timer(pygame.USEREVENT + 5, 40)
            elif self.jumptime == 8:
                self.unjumping = True
                self.speed[1] = 2
                pygame.time.set_timer(pygame.USEREVENT + 5, 40)
            else:
                pygame.time.set_timer(pygame.USEREVENT + 5, 40)
        else:
            if self.jumptime == 2:
                self.jumptime -=2
                pygame.time.set_timer(pygame.USEREVENT + 5, 0)
                self.speed[1] = 0
                self.unjumping = False
                self.jumping = False
            else:
                self.jumptime -= 1
                pygame.time.set_timer(pygame.USEREVENT + 5, 40)"""
    