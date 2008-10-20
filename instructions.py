import sys, pygame
from pygame.locals import *

class instructions():
    def __init__(self, font, size):
        self.font = font
        self.width = size[0]
        self.height= size[1]
        self.rendered = []
        self.poses = []
        self.howtos = ("                     Instructions"
                       , ""
                       , "     To move around, use the arrow keys"
                       , "         on your keyboard"
                       , ""
                       , "     Special skills:"
                       , "            A - physical attack"
                      # , "            S - magic shield => 45 Mana"
                       , "            D - iron shield (defend)"
                       , "            F - shoot fireballs => 20 Mana"
                       , ""
                       , "     Press [Spacebar] to jump"
                       , ""
                       , "     Pressing [Backspace] returns you to"
                       , "         main menu while you're playing"
                       , ""
                       , "  Press [Enter] to return to the main menu")
        for string in range(0,len(self.howtos)):
            self.rendered.append(self.font.render(self.howtos[string], 1, (255, 255, 255)))
        for num in range(0, len(self.howtos)):
            self.poses.append((self.width / 2 - 240, self.height / 2 - (-num * 25) - 225))
        self.pointloc = 0
        self.pointpos = [self.width / 2 - 80, self.poses[self.pointloc][1] + 5]

def show_howto(font, screen, size, background):
    instr = instructions(font, size)
    screen.blit(background, (0, 0))
    for item, pos in zip(instr.rendered, instr.poses):
        screen.blit(item, pos)
    pygame.display.flip()
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return
                
    