import pygame
from pygame.locals import *
from fireball import *

Normal = 0
Defend = 1
Attack = 2
Fire = 3
MS = 4

class Player(pygame.sprite.Sprite):
    def __init__(self, animations):
        pygame.sprite.Sprite.__init__(self)
    def attack(self, attackorz):
        if attackorz:
            self.special = True
            self.image = self.atkanim[self.atktime]
            self.atktime += 1
            pygame.time.set_timer(pygame.USEREVENT + 1, 40)
            if self.atktime == 4:
                self.attacking = True
                pygame.time.set_timer(pygame.USEREVENT + 1, 40)
            elif self.atktime == 7:
                self.unattacking = True
                pygame.time.set_timer(pygame.USEREVENT + 1, 40)
            else:
                pygame.time.set_timer(pygame.USEREVENT + 1, 40)
        else:
            if self.atktime == 0:
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)
                self.unattacking = False
                self.image = self.old
                self.special = False
            else:
                self.atktime -= 1
                self.image = self.atkanim[self.atktime]
                pygame.time.set_timer(pygame.USEREVENT + 1, 40)
                if self.atktime == 3:
                    self.attacking = False
    
    def defend(self, defendorz):
        if defendorz:
            self.special = True
            self.image = self.defanim[self.deftime]
            self.deftime += 1
            if self.deftime == 6:
                self.defending = True
                self.undefending = True
                pygame.time.set_timer(pygame.USEREVENT + 2, 500)
            else:
                pygame.time.set_timer(pygame.USEREVENT + 2, 40)
        else:
            if self.deftime == 0:
                pygame.time.set_timer(pygame.USEREVENT + 2, 0)
                self.undefending = False
                self.image = self.old
                self.special = False
            else:
                self.deftime -= 1
                self.image = self.defanim[self.deftime]
                pygame.time.set_timer(pygame.USEREVENT + 2, 40)
    def fire(self, firezorz):
        if firezorz:
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
                pygame.time.set_timer(pygame.USEREVENT + 3, 90)
    
    def magic_shield(self, magicorz):
        if magicorz:
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
                pygame.time.set_timer(pygame.USEREVENT + 4, 40)
    
    def jump(self, jumporz):
        if jumporz:
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
                pygame.time.set_timer(pygame.USEREVENT + 5, 40)
    
    def move(self, key):
        if (key == K_RIGHT):
            self.speed[0] = 2
        elif (key == K_LEFT):
            self.speed[0] = -2
        elif (key == K_UP):
            self.speed[1] = -2
        elif (key == K_DOWN):
            self.speed[1] = 2
    
    def stop_ud(self):
        self.speed[1] = 0
    def stop_lr(self):
        self.speed[0] = 0
    
    def refresh(self):
        self.counter += 1
        if (self.mana < 100) and (self.counter % 100 == 0):
            self.mana += 1
        temp = self.pos.move(self.speed)
        if (temp.right > self.screen[0]):
            self.pos.right = self.screen[0]
            self.speed[0] = 0
        elif (temp.left < 0):
            self.pos.left = 0
            self.speed[0] = 0
        elif ((temp.top < ((self.screen[1] * 5) / 8)) and not self.jumping):
            self.pos.top = (self.screen[1] * 5) / 8
            self.speed[1] = 0
        elif (temp.bottom > self.screen[1]):
            self.pos.bottom = self.screen[1]
            self.speed[1] = 0
        else:
            self.pos = temp
    
    def pass_bottom(self, other):
        return self.pos.bottom > other.pos.top and self.pos.bottom < other.pos.bottom
    
    def pass_top(self, other):
        return  self.pos.top > other.pos.top and self.pos.top < other.pos.bottom
    
    def pass_left(self, other):
        return self.pos.left > other.pos.left and self.pos.left < other.pos.right
    
    def pass_right(self, other):
        return self.pos.right > other.pos.left and self.pos.right < other.pos.right
    
    def pass_between(self, other):
        return self.pos.top < other.pos.top and self.pos.bottom > other.pos.bottom
    
    def touch(self, other):
        # Check if boxes touch each other, not if they are
        # in the EXACT same position, because it's almost impossible
        # to do that with others. This also doesn't match the
        # images because the image boxes are larger than the
        # visible part of the image.
        # also changed from binary & to more efficient (and safer), logical 'and'
        # same as difference between & and && in c and c++
        #return (self.pos.left == other.pos.left) & (self.pos.top == other.pos.top)
        return (self.pass_bottom(other) and self.pass_left(other)) or (self.pass_bottom(other) and self.pass_right(other)) or (self.pass_top(other) and self.pass_left(other)) or (self.pass_top(other) and self.pass_right(other)) or (self.pass_between(other) and self.pass_left(other)) or (self.pass_between(other) and self.pass_right(other))
