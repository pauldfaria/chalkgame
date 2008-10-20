import pygame
from player import *

class Item(Player):
    
    def __init__(self, animations, name, health, strength, drop, screen = (1024, 768)):
        Player.__init__(self, animations, screen)
        self.last_anim = self.norm
        self.name = name
        self.health = health
        self.strength = strength
        self.drop = drop
    
    def attack(self):
        if self.last_anim != self.atkanim:
            self.animation.reset()
            self.last_anim = self.atkanim
        Player.attack(self)
    
    def move(self, speed):
        if self.last_anim != self.movanim:
            self.animation.reset()
            self.last_anim = self.movanim
        Player.move(self)
        self.speed = speed
    
    def refresh(self):
        Player.refresh(self)
