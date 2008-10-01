import pygame

class Fireball(pygame.sprite.Sprite):
    
    def __init__(self, image, pos, edge):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.speed = (5, 0)
        self.pos = pos
        self.edge = edge
    
    def refresh(self):
        if(self.pos.left > self.edge):
            self.kill()
        else:
            self.pos = self.pos.move(self.speed)
    
    def change_speed(self, newspeed):
        self.speed = newspeed
