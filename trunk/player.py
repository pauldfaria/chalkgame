import pygame
from pygame.locals import *
from fireball import *
from animation import *

Normal = 0
Defend = 1
Attack = 2

class Player(pygame.sprite.Sprite):
    def __init__(self, animations, screen = (1024, 768)):
        pygame.sprite.Sprite.__init__(self)
        self.animation = Animation()
        self.animate = False
        self.animations = animations
        
        #normal variables
        self.normanim = self.animations[Normal][0]
        self.normframes = self.animations[Normal][1]
        self.curanim = self.normanim
        self.frames = self.normframes
        self.norm = self.normanim.subsurface(Rect(self.normanim.get_rect().left,
                                                   self.normanim.get_rect().top,
                                                   self.normanim.get_rect().width / self.frames,
                                                   self.normanim.get_rect().height))
        self.image = self.norm
        self.frame = 0
        
        #defending variables
        self.defanim = self.animations[Defend][0]
        self.defframes = self.animations[Defend][1]
        self.deftime = 0
        self.defending = False
        
        #attacking variables
        self.atkanim = self.animations[Attack][0]
        self.atkframes = self.animations[Attack][1]
        self.atktime = 0
        self.attacking = False
        
        #position/speed variables
        self.speed = [0, 0]
        self.pos = self.image.get_rect().move(0, screen[1])
        self.screen = screen
        
        #special variables
        self.special = False
        self.health = 100
        self.mana = 100
        self.counter = 0
        self.end = False
    
    def attack(self):
        self.attacking = True
        self.curanim = self.atkanim
        self.frames = self.atkframes
        self.animate = True
        self.end = True
    
    def defend(self):
        self.defending = True
        self.curanim = self.defanim
        self.frames = self.defframes
        self.animate = True
        self.end = False
    
    def move(self, key):
        self.animate = True
        self.curanim = self.normanim
        self.curframes = self.normframes
        self.end = False
        if key == K_RIGHT:
            self.speed[0] = 6
        elif key == K_LEFT:
            self.speed[0] = -6
        elif key == K_UP:
            self.speed[1] = -6
        elif key == K_DOWN:
            self.speed[1] = 6
    
    def stop_ud(self):
        self.end = True
        self.speed[1] = 0
    def stop_lr(self):
        self.end = True
        self.speed[0] = 0
        
    def refresh(self):
        self.counter += 1
        if (self.mana < 100) and (self.counter % 100 == 0):
            self.mana += 1
        temp = self.pos.move(self.speed)
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
            self.pos = temp
        if self.animate and (self.counter % 5 == 0):
            (self.image, self.frame, self.animate) = self.animation.animate(self.curanim
                                                                        , self.frames, self.end)
            if not self.animate:
                self.attacking = False
                self.defending = False
        elif self.counter % 5 == 0:
            self.image = self.norm
    
    
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
        return ((self.pass_bottom(other) and self.pass_left(other))
            or (self.pass_bottom(other) and self.pass_right(other))
            or (self.pass_top(other) and self.pass_left(other))
            or (self.pass_top(other) and self.pass_right(other))
            or (self.pass_between(other) and self.pass_left(other))
            or (self.pass_between(other) and self.pass_right(other)))