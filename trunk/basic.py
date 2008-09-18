import sys, pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    
    def __init__(self, image, defend, attack, throwfire, fireball, screen = (640, 480)):
        pygame.sprite.Sprite.__init__(self)
        self.old = image
        self.image = image
        self.defanim = defend
        self.deftime = 0
        self.defending = False
        self.undefending = False
        self.atkanim = attack
        self.atktime = 0
        self.fireanim = throwfire
        self.firetime = 0
        self.fireball = fireball
        self.speed = [0, 0]
        self.pos = image.get_rect().move(0, screen[1])
        self.screen = screen
        self.special = False
    
    def camo(self):
        self.special = True
        self.image = pygame.Surface((0, 0))
    
    def attack(self):
        self.special = True
        self.image = self.atkanim[self.atktime]
        self.atktime += 1
        if self.atktime == 7:
            self.atktime = 0
            pygame.time.set_timer(pygame.USEREVENT + 5, 0)
            pygame.time.set_timer(pygame.USEREVENT + 4, 40)
        else:
            pygame.time.set_timer(pygame.USEREVENT + 5, 40)
    
    def defend(self, defend):
        if defend == True:
            self.special = True
            self.image = self.defanim[self.deftime]
            self.deftime += 1
            if self.deftime == 6:
                pygame.time.set_timer(pygame.USEREVENT + 6, 0)
                self.defending = True
            else:
                pygame.time.set_timer(pygame.USEREVENT + 6, 30)
        else:
            if self.deftime == 0:
                pygame.time.set_timer(pygame.USEREVENT + 6, 0)
                self.undefending = False
                self.image = self.old
                self.special = False
            else:
                self.undefending = True
                self.deftime -= 1
                self.image = self.defanim[self.deftime]
                pygame.time.set_timer(pygame.USEREVENT + 6, 30)
    
    def fire(self, fire):
        if fire == True:
            self.special = True
            self.firing = True
            self.image = self.fireanim[self.firetime]
            self.firetime += 1
            pygame.time.set_timer(pygame.USEREVENT + 7, 30)
            if self.firetime == 3:
                fireball = Fireball(self.fireball, self.pos.move(10, 25) , self.screen[0])
                self.firing = False
                return fireball
        else:
            if self.firetime == 0:
                pygame.time.set_timer(pygame.USEREVENT + 7, 0)
                self.image = self.old
                self.special = False
            else:
                self.firetime -= 1
                self.image = self.fireanim[self.firetime]
                pygame.time.set_timer(pygame.USEREVENT + 7, 30)
            
    
    def be_normal(self):
        pygame.time.set_timer(pygame.USEREVENT + 4, 0)
        self.image = self.old
        self.special = False
    
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
        temp = self.pos.move(self.speed)
        if (temp.right > self.screen[0]):
            self.pos.right = self.screen[0]
            self.speed[0] = 0
        elif (temp.left < 0):
            self.pos.left = 0
            self.speed[0] = 0
        elif (temp.top < (self.screen[1] * 5) / 8):
            self.pos.top = (self.screen[1] * 5) / 8
            self.speed[1] = 0
        elif (temp.bottom > self.screen[1]):
            self.pos.bottom = self.screen[1]
            self.speed[1] = 0
        else:
            self.pos = temp

class Fireball(pygame.sprite.Sprite):
    
    def __init__(self, image, pos, edge):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.speed = [5, 0]
        self.pos = pos
        self.edge = edge
    
    def refresh(self):
        if(self.pos.left > self.edge):
            self.kill()
        else:
            self.pos = self.pos.move(self.speed)

def main():
    pygame.init()
    
    size = width, height = 640, 480
    screen = pygame.display.set_mode(size)
    attack = (pygame.image.load('images/player2_attack0.gif').convert()
              , pygame.image.load('images/player2_attack1.gif').convert()
              , pygame.image.load('images/player2_attack2.gif').convert()
              , pygame.image.load('images/player2_attack3.gif').convert()
              , pygame.image.load('images/player2_attack4.gif').convert()
              , pygame.image.load('images/player2_attack5.gif').convert()
              , pygame.image.load('images/player2_attack6.gif').convert())
    defend = (pygame.image.load('images/player2_defend0.gif').convert()
              ,pygame.image.load('images/player2_defend1.gif').convert()
              ,pygame.image.load('images/player2_defend2.gif').convert()
              ,pygame.image.load('images/player2_defend3.gif').convert()
              ,pygame.image.load('images/player2_defend4.gif').convert()
              ,pygame.image.load('images/player2_defend5.gif').convert())
    fire = (pygame.image.load('images/player2_fire0.gif').convert()
            ,pygame.image.load('images/player2_fire1.gif').convert()
            ,pygame.image.load('images/player2_fire1.gif').convert())
    
    background = pygame.image.load('images/background.bmp').convert()
    fireball = pygame.image.load('images/fireball2.gif').convert()
    player = Player(pygame.image.load('images/player2.gif').convert(), defend
                    , attack , fire,fireball, size)
    
    del attack
    del defend
    
    offset = 0
    current_lr = current_ud = "fubar"
    
    fireballs = []
    
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if((event.key == K_LEFT) or (event.key == K_RIGHT)):
                    current_lr = event.key
                    player.move(event.key)
                elif((event.key == K_UP) or (event.key == K_DOWN)):
                    current_ud = event.key
                    player.move(event.key)
                elif (((event.key == K_SPACE) or (event.key == K_f)) and (not player.special)):
                    player.fire(True)
                elif ((event.key == K_d) and (not player.special)):
                    player.defend(True)
                elif ((event.key == K_a) and (not player.special)):
                    player.attack()
                elif ((event.key == K_c) and (not player.special)):
                    player.camo()
            
            elif event.type == pygame.KEYUP:
                if(((event.key == K_LEFT) or (event.key == K_RIGHT)) and (current_lr == event.key)):
                   player.stop_lr()
                elif(((event.key == K_UP) or (event.key == K_DOWN)) and (current_ud == event.key)):
                    player.stop_ud()
                elif (event.key == K_c):
                    player.be_normal()
                elif (event.key == K_d):
                    player.defend(False)
            
            elif event.type == pygame.USEREVENT + 4:
                player.be_normal()
            
            elif event.type == pygame.USEREVENT + 5:
                player.attack()
            
            elif event.type == pygame.USEREVENT + 6:
                if not player.undefending:
                    player.defend(True)
                else:
                    player.defend(False)
            
            elif event.type == pygame.USEREVENT + 7:
                if not player.firing:
                    player.fire(False)
                elif player.firetime == 2:
                        fireballs.append(player.fire(True))
                else:
                    player.fire(True)
        
        player.refresh()
        if (player.pos.right >= (width * 5) / 8):
            offset -= 2
            player.pos.right = (width * 5) / 8 - 1
            for fireball in fireballs:
                fireball.speed = [3, 0]
        else:
            for fireball in fireballs:
                fireball.speed = [5, 0]
        
        if -offset > width:
            offset = 0
        
        screen.blit(background, (offset, 0))
        screen.blit(background, (offset + width, 0))
        
        for fireball in fireballs:
            fireball.refresh()
            screen.blit(fireball.image, fireball.pos)
        screen.blit(player.image, player.pos)
        
        pygame.display.flip()
        pygame.time.delay(5)

if __name__ == "__main__":
    main()