import pygame
from pygame.locals import *
from fireball import *
from animation import *
from random import *

Normal = 0
Attack = 1

class Player(pygame.sprite.Sprite):
    def __init__(self, animations, screen = (1024, 768)):
        pygame.sprite.Sprite.__init__(self)
        self.animation = Animation()
        self.animate = False
        self.animations = animations
        
        #normal variables
        self.movanim = self.animations[Normal][0]
        self.movframes = self.animations[Normal][1]
        self.curanim = self.movanim
        self.frames = self.movframes
        self.norm = self.movanim.subsurface(Rect(self.movanim.get_rect().left,
                                                   self.movanim.get_rect().top,
                                                   self.movanim.get_rect().width / self.frames,
                                                   self.movanim.get_rect().height))
        self.image = self.norm
        self.frame = 0
        
        #attacking variables
        self.atkanim = self.animations[Attack][0]
        self.atkframes = self.animations[Attack][1]
        self.damageframe = self.animations[Attack][2]
        self.atktime = 0
        self.attacking = False
        self.modifier = 1
        
        #position/speed variables
        self.speed = [0, 0]
        self.pos = self.image.get_rect().move(0, screen[1])
        self.screen = screen
        
        #special variables
        self.health = 100
        self.counter = 0
        self.end = False
    
    def attack(self):
        self.attacking = True
        self.curanim = self.atkanim
        self.frames = self.atkframes
        self.animate = True
        self.end = True

    def do_damage(self, other):
        self.attacking = True
        self.curanim = self.atkanim
        self.frames = self.atkframes
        self.animate = True
        damage = randint(50,150) * self.strength / 100
        if damage % 2 == 1:
            damage -= 1
        damage = int( damage * self.modifier )
        other.health -= damage
        self.end = True
        self.modifier = 1
        return damage
    
    def move(self):
        self.attacking = False
        self.animate = True
        self.curanim = self.movanim
        self.frames = self.movframes
        self.end = False
    
    def stop_ud(self):
        self.end = True
        self.speed[1] = 0
    def stop_lr(self):
        self.end = True
        self.speed[0] = 0
    
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
    
    def refresh(self):
        self.counter += 1
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
            (self.image, self.frame, self.animate) = self.animation.animate(self.curanim, self.frames, self.end)
        elif self.counter % 5 == 0:
            self.image = self.norm
