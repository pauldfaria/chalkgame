import sys, pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    """This class defines the human controlled character"""
    
    """standard initialization"""
    def __init__(self, image, defimage, atkimage, throwfire, fireball, screen = (640, 480)):
        pygame.sprite.Sprite.__init__(self)
        self.old = image
        self.image = image
        self.defimage = defimage
        self.atkimage = atkimage
        self.throwfire = throwfire
        self.fireball = fireball
        self.speed = [0, 0]
        self.pos = image.get_rect().move(0, screen[1])
        self.screen = screen
        self.jumpimg = False
    
    def camo(self):
        self.image = pygame.Surface((0, 0))
    
    def defend(self):
        self.image = self.defimage
    
    def attack(self):
        self.image = self.atkimage
        pygame.time.set_timer(pygame.USEREVENT + 4, 250)
    
    def fire(self):
        """shoot a fireball"""
        self.image = self.throwfire
        pygame.time.set_timer(pygame.USEREVENT + 4, 150)
        fireball = Fireball(self.fireball, self.pos.move(-3, 10), self.screen[0])
        return fireball
    
    def be_normal(self):
        pygame.time.set_timer(pygame.USEREVENT + 4, 0)
        self.image = self.old
    
    """allows the player to move left and right"""
    def move(self, key):
        if (key == K_RIGHT):
            self.speed[0] = 3
        elif (key == K_LEFT):
            self.speed[0] = -3
    
    """allows the player to jump only when he is
    touching the floor"""
    def jump(self):
        if (not self.jumping):
            self.jumping = True
            self.speed[1] = -2
            pygame.time.set_timer(pygame.USEREVENT, 250)
    
    """the following 3 functions are used to make
    the jump look 'nicer'"""
    def hover_up(self):
        self.speed[1] = -1
        pygame.time.set_timer(pygame.USEREVENT, 0)
        pygame.time.set_timer(pygame.USEREVENT + 1, 125)
    
    def hover(self):
        self.speed[1] = 0
        pygame.time.set_timer(pygame.USEREVENT + 1, 0)
        pygame.time.set_timer(pygame.USEREVENT + 2, 50)
    
    def hover_down(self):
        self.speed[1] = 1
        pygame.time.set_timer(pygame.USEREVENT + 2, 0)
        pygame.time.set_timer(pygame.USEREVENT + 3, 125)
    
    """this makes the player fall"""
    def fall(self):
        self.speed[1] = 2
        pygame.time.set_timer(pygame.USEREVENT + 3, 0)
    
    """this makes the player stop moving left and right"""
    def stop(self):
        self.speed[0] = 0
    
    """this allows the player to keep moving
    in his current direction until the player
    reaches a wall"""
    def refresh(self):
        temp = self.pos.move(self.speed)
        if (temp.right > self.screen[0]):
            self.pos.right = self.screen[0]
            self.speed[0] = 0
        elif (temp.left < 0):
            self.pos.left = 0
            self.speed[0] = 0
        elif (temp.top < 0):
            self.pos.top = 0
        elif (temp.bottom > self.screen[1]):
            self.pos.bottom = self.screen[1]
            self.speed[1] = 0
            self.jumping = False
        else:
            self.pos = temp

class Fireball(pygame.sprite.Sprite):
    
    def __init__(self, image, pos, edge):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.speed = (5, 0)
        self.pos = pos
        self.edge = edge
    
    def refresh(self):
        if(self.pos.left > self.  edge):
            self.kill()
        else:
            self.pos = self.pos.move(self.speed)

def main():
    pygame.init()
    
    size = width, height = 640, 480
    screen = pygame.display.set_mode(size)
    
    background = pygame.image.load('images/background.bmp').convert()
    fireball = pygame.image.load('images/fireball2.gif').convert()
    player = Player(pygame.image.load('images/player.gif').convert()
                    , pygame.image.load('images/player_block.gif').convert()
                    , pygame.image.load('images/player_sword.gif').convert()
                    , pygame.image.load('images/player_fire.gif').convert()
                    ,fireball, size)
    
    offset = 0
    current = "fubar"
    
    fireballs = []
    
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            
            elif event.type == KEYDOWN:
                if ((event.key == K_LEFT) or (event.key == K_RIGHT)):
                    current = event.key
                    player.move(event.key)
                elif (event.key == K_UP):
                    player.jump()
                elif (event.key == K_SPACE):
                    fireballs.append(player.fire())
                elif (event.key == K_d):
                    player.defend()
                elif (event.key == K_a):
                    player.attack()
                elif (event.key == K_c):
                    player.camo()
            
            elif event.type == pygame.KEYUP:
                if (((event.key == K_LEFT) or (event.key == K_RIGHT)) and (event.key == current)):
                    player.stop()
                elif ((event.key == K_d) or (event.key == K_c)):
                    player.be_normal()
            
            elif event.type == pygame.USEREVENT:
                player.hover_up()
            
            elif event.type == pygame.USEREVENT + 1:
                player.hover()
            
            elif event.type == pygame.USEREVENT + 2:
                player.hover_down()
            
            elif event.type == pygame.USEREVENT + 3:
                player.fall()
            
            elif event.type == pygame.USEREVENT + 4:
                player.be_normal()
        
        if -offset > width:
            offset = 0
        
        screen.blit(background, (offset, 0))
        screen.blit(background, (offset + width, 0))
        offset -= 1
        
        for fireball in fireballs:
            fireball.refresh()
            screen.blit(fireball.image, fireball.pos)
        player.refresh()
        screen.blit(player.image, player.pos)
        
        pygame.display.flip()
        pygame.time.delay(5)

if __name__ == "__main__":
    main()