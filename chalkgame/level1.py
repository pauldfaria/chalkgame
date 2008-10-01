import sys, pygame
from pygame.locals import *
from human import *
from fireball import *

def level1(size, screen, background):
    width = size[0]
    height = size[1]
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
    
    fireball = pygame.image.load('images/fireball.gif').convert()
    player1 = Human((pygame.image.load('images/player2.gif').convert(), defend
                    , attack , fire, ms), fireball, size)
    
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
                if (event.key == K_LEFT) or (event.key == K_RIGHT):
                    current_lr = event.key
                    player1.move(event.key)
                elif (event.key == K_UP) or (event.key == K_DOWN):
                    current_ud = event.key
                    player1.move(event.key)
                elif (((event.key == K_SPACE) or (event.key == K_f)) and (not player1.special)):
                    if player1.mana > 19:
                        player1.fire(True)
                elif ((event.key == K_d) and (not player1.special)):
                    player1.defend(True)
                elif ((event.key == K_a) and (not player1.special)):
                    player1.attack(True)
                elif ((event.key == K_s) and (not player1.special)):
                    if player1.mana > 44:
                        player1.magic_shield(True)
                elif event.key == K_BACKSPACE:
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)
                    pygame.time.set_timer(pygame.USEREVENT + 2, 0)
                    pygame.time.set_timer(pygame.USEREVENT + 3, 0)
                    pygame.time.set_timer(pygame.USEREVENT + 4, 0)
                    return
            
            elif event.type == pygame.KEYUP:
                if(((event.key == K_LEFT) or (event.key == K_RIGHT))
                   and (current_lr == event.key)):
                   player1.stop_lr()
                elif(((event.key == K_UP) or (event.key == K_DOWN))
                     and (current_ud == event.key)):
                    player1.stop_ud()
            
            elif event.type == pygame.USEREVENT + 1:
                if not player1.unattacking:
                    player1.attack(True)
                else:
                    player1.attack(False)
            
            elif event.type == pygame.USEREVENT + 2:
                if not player1.undefending:
                    player1.defend(True)
                else:
                    player1.defend(False)
            
            elif event.type == pygame.USEREVENT + 3:
                if not player1.firing:
                    player1.fire(False)
                elif player1.firetime == 2:
                        fireballs.append(player1.fire(True))
                else:
                    player1.fire(True)
            
            elif event.type == pygame.USEREVENT + 4:
                if not player1.unmsing:
                    player1.magic_shield(True)
                else:
                    player1.magic_shield(False)
        
        player1.refresh()
        if (player1.pos.right >= (width * 5) / 8):
            offset -= 2
            player1.pos.right = (width * 5) / 8 - 1
            for fireball in fireballs:
                fireball.change_speed((3,0))
        else:
            for fireball in fireballs:
                fireball.change_speed((5,0))
        
        if -offset > width:
            offset = 0
        
        screen.blit(background, (offset, 0))
        screen.blit(background, (offset + width, 0))
        
        if pygame.font:
            font = pygame.font.Font(None, 36)
            texthp = font.render("Health: %s" % player1.health , 1, (255, 255, 255))
            textmp = font.render("Mana: %s" % player1.mana, 1, (255, 255, 255))
            textposhp = [0, 0]
            textposmp = [0, 20]
            screen.blit(texthp, textposhp)
            screen.blit(textmp, textposmp)
        
        for fireball in fireballs:
            fireball.refresh()
            screen.blit(fireball.image, fireball.pos)
        screen.blit(player1.image, player1.pos)
        
        pygame.display.flip()
        pygame.time.delay(5)

if __name__ == "__main__":
    main()