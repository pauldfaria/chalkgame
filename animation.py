import pygame
from pygame.locals import *

class Animation():
    def __init__(self):
        self.cur_frame = 0
    
    def reset(self):
        self.cur_frame = 0
    
    def animate(self, animation, frames, end):
        rect = animation.get_rect()
        animate = True
        frame_width = rect.width / frames
        image = animation.subsurface(Rect((frame_width * self.cur_frame, rect.top), (frame_width, rect.height)))
        if self.cur_frame >= frames - 1:
            self.cur_frame = 0
            animate = not end
        else:
            self.cur_frame += 1

        
        return (image, self.cur_frame, animate)
    
    #to be used for latta 
    """def reverse_animate(self, animation, frames, end):
        rect = animation.get_rect()
        animate = True
        frame_width = rect.width / frames
        image = animation.subsurface(Rect((frame_width * self.cur_frame, rect.top), (frame_width, rect.height)))
        if (self.cur_frame == 0):
            animate = not end
        else:
            self.cur_frame -= 1
        
        return (image, self.cur_frame, animate)"""
