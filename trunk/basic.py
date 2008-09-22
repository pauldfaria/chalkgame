#!/usr/bin/python

import sys, pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    
    def __init__(self, image, defend, attack, throwfire
                 , fireball, ms, screen = (640, 480)):
        pygame.sprite.Sprite.__init__(self)
        self.old = image
        self.image = image
        self.defanim = defend
        self.deftime = 0
        self.defending = False
        self.undefending = False
        self.atkanim = attack
        self.atktime = 0
        self.attacking = False
        self.unattacking = False
        self.fireanim = throwfire
        self.firetime = 0
        self.fireball = fireball
        self.msanim = ms
        self.mstime = 0
        self.msing = False
        self.unmsing = False
        self.speed = [0, 0]
        self.pos = image.get_rect().move(0, screen[1])
        self.screen = screen
        self.special = False
        self.health = 100
        self.mana = 100
        self.counter = 0
    
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
              , pygame.image.load('images/player2_defend1.gif').convert()
              , pygame.image.load('images/player2_defend2.gif').convert()
              , pygame.image.load('images/player2_defend3.gif').convert()
              , pygame.image.load('images/player2_defend4.gif').convert()
              , pygame.image.load('images/player2_defend5.gif').convert())
    fire = (pygame.image.load('images/player2_fire0.gif').convert()
            , pygame.image.load('images/player2_fire1.gif').convert()
            , pygame.image.load('images/player2_fire1.gif').convert())
    ms = (pygame.image.load('images/player2_ms0.gif').convert()
          , pygame.image.load('images/player2_ms1.gif').convert()
          , pygame.image.load('images/player2_ms2.gif').convert()
          , pygame.image.load('images/player2_ms3.gif').convert()
          , pygame.image.load('images/player2_ms4.gif').convert()
          , pygame.image.load('images/player2_ms5.gif').convert()
          , pygame.image.load('images/player2_ms6.gif').convert()
          , pygame.image.load('images/player2_ms7.gif').convert()
          , pygame.image.load('images/player2_ms8.gif').convert())
    
    background = pygame.image.load('images/background.bmp').convert()
    fireball = pygame.image.load('images/fireball.gif').convert()
    player = Player(pygame.image.load('images/player2.gif').convert(), defend
                    , attack , fire, fireball, ms, size)
    
    del attack
    del defend
    del fire
    del ms
    
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
                    if player.mana > 19:
                        print player.mana
                        player.fire(True)
                    else:
                        pass
                elif ((event.key == K_d) and (not player.special)):
                    player.defend(True)
                elif ((event.key == K_a) and (not player.special)):
                    player.attack(True)
                elif ((event.key == K_s) and (not player.special)):
                    player.magic_shield(True)
            
            elif event.type == pygame.KEYUP:
                if(((event.key == K_LEFT) or (event.key == K_RIGHT)) and (current_lr == event.key)):
                   player.stop_lr()
                elif(((event.key == K_UP) or (event.key == K_DOWN)) and (current_ud == event.key)):
                    player.stop_ud()
            
            elif event.type == pygame.USEREVENT + 1:
                if not player.unattacking:
                    player.attack(True)
                else:
                    player.attack(False)
            
            elif event.type == pygame.USEREVENT + 2:
                if not player.undefending:
                    player.defend(True)
                else:
                    player.defend(False)
            
            elif event.type == pygame.USEREVENT + 3:
                if not player.firing:
                    player.fire(False)
                elif player.firetime == 2:
                        fireballs.append(player.fire(True))
                else:
                    player.fire(True)
            
            elif event.type == pygame.USEREVENT + 4:
                if not player.unmsing:
                    player.magic_shield(True)
                else:
                    player.magic_shield(False)
        
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
        
        if pygame.font:
            font = pygame.font.Font(None, 36)
            texthp = font.render("Health: %s" % player.health , 1, (0, 0, 0))
            textmp = font.render("Mana: %s" % player.mana, 1, (0, 0, 0))
            textposhp = [0, 0]
            textposmp = [0, 20]
            screen.blit(texthp, textposhp)
            screen.blit(textmp, textposmp)
        
        for fireball in fireballs:
            fireball.refresh()
            screen.blit(fireball.image, fireball.pos)
        screen.blit(player.image, player.pos)
        
        pygame.display.flip()
        pygame.time.delay(5)

if __name__ == "__main__":
    main()
