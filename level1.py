import sys, pygame
from pygame.locals import *
from human import *
from fireball import *
from monster import *
from random import *

def level1(size, screen, background):
    boxx = False
    
    width = size[0]
    height = size[1]
    normal = (pygame.image.load('images/hero1walk.png').convert_alpha(), 4)
    attack = (pygame.image.load('images/hero1attack.png').convert_alpha(), 4, 3)
    defend = (pygame.image.load('images/hero1block.png').convert_alpha(), 1)
    fire = (pygame.image.load('images/hero1magic.png').convert_alpha(), 19)
    jump = (pygame.image.load('images/hero1jump.png').convert_alpha(), 10)
    fireball = pygame.image.load('images/fireball.gif').convert_alpha()
    
    plus = (pygame.image.load('images/pluswalk.png').convert_alpha(), 13)
    patk = (pygame.image.load('images/plusattack.png').convert_alpha(), 12, 9)
    
    tri = (pygame.image.load('images/trianglewalk.png').convert_alpha(), 6)
    triatk = (pygame.image.load('images/triangleattack.png').convert_alpha(), 7, 6)
    
    frac = (pygame.image.load('images/fractionwalk.png').convert_alpha(), 8)
    
    enemy = 0
    
    player1 = Human((normal, defend, attack , fire, jump), fireball, size)
    boximg = pygame.image.load('images/box.gif').convert()
    
    del normal
    del attack
    del defend
    del fire
    del jump
    
    offset = 0
    current_lr = current_ud = "fubar"
    
    fireballs = []
    
    while player1.health > 0:
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
                elif (event.key == K_f) and not player1.special:
                    if player1.mana > 19:
                        player1.fire()
                elif event.key == K_SPACE:
                    player1.jump()
                elif (event.key == K_d) and not player1.special:
                    player1.defend()
                elif (event.key == K_a) and not player1.special:
                    player1.attack()
                    #elif (event.key == K_s) and not player1.special:
                    #if player1.mana > 44:
                    #    player1.magic_shield()
                elif event.key == K_BACKSPACE:
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)
                    pygame.time.set_timer(pygame.USEREVENT + 2, 0)
                    pygame.time.set_timer(pygame.USEREVENT + 3, 0)
                    pygame.time.set_timer(pygame.USEREVENT + 4, 0)
                    pygame.time.set_timer(pygame.USEREVENT + 5, 0)
                    return
            
            elif event.type == pygame.KEYUP:
                if ((event.key == K_LEFT) or (event.key == K_RIGHT)
                   and (current_lr == event.key)):
                   player1.stop_lr()
                elif ((event.key == K_UP) or (event.key == K_DOWN)
                     and (current_ud == event.key)):
                    player1.stop_ud()
                elif event.key == K_d:
                    player1.stop_defending()
                    
        # consider putting in a for loop going through all the "players"
        if (boxx):
            #boxx=box.refresh()
            box.refresh()
            
            #box.pos.right -= player1.speed[0]
            #box.move([-player1.speed[0], 0])
            
            # these if statements make the box "chase" the player
            if ((box.pos.right + box.pos.left) > (player1.pos.right + player1.pos.left)):
                box.speed[0] = -1
            else:
                box.speed[0] = 1
            if ((box.pos.top + box.pos.bottom) < (player1.pos.top + player1.pos.bottom)):
                box.speed[1] = 1
            else:
                box.speed[1] = -1
            if player1.touch(box):
                box.speed = [0,0]
            # it's pretty stupid actually 
                
            
            # only remove if player has attacked the "box"
            # also kill the box, not move it off screen
            # this keeps us from having memory leaks
            if player1.touch(box):
                if player1.attacking and player1.animation.cur_frame == player1.damageframe and player1.counter % 5 == 0:
                    boxx = False
                    box.kill()
                    player1.kills += 1
                if (not player1.defending) and box.attacking and box.animation.cur_frame == box.damageframe and box.counter % 5 == 0:
                    player1.health -= box.strength
                    if player1.health < 0:
                        player1.health = 0
                else:
                    box.attack()
            else:
                for fireball in fireballs:
                    if (box.touch(fireball)):
                        boxx = False
                        box.kill()
                        player1.kills += 1
                        fireball.kill()
        
        player1.refresh()
        if (player1.pos.right >= (width * 5) / 8):
            offset -= 6
            player1.pos.right = (width * 5) / 8 - 1
            if boxx:
                box.speed[0] -= 6
            elif randint(0,10) == 1:
                enemy = randint(1,3)
                if enemy == 1:
                    box = Monster((plus, (boximg,1), patk), 10, size)
                elif enemy == 2:
                    box = Monster((tri, (boximg, 1), triatk), 15, size)
                else:
                    box = Monster((frac, (boximg, 1), triatk), 5, size)
                #box.pos=box.image.get_rect().move(width, (randint((height * 5 / 8),height)))
                box.move([width, randint((height * 5 / 8), height)])
                boxx = True
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
            texthp = font.render("Health: %s" % player1.health, 1, (0, 255, 0))
            textmp = font.render("Mana: %s" % player1.mana, 1, (0, 0, 255))
            textkills = font.render("Kills: %s" % player1.kills, 1, (255, 0, 0))
            textposhp = [0, 0]
            textposmp = [0, 20]
            textposkills = [0, 40]
            screen.blit(texthp, textposhp)
            screen.blit(textmp, textposmp)
            screen.blit(textkills, textposkills)
        
        for fireball in fireballs:
            fireball.refresh()
            screen.blit(fireball.image, fireball.pos)
        screen.blit(player1.image, player1.pos)
        
        if (boxx):
            screen.blit(box.image, box.pos)
        
        pygame.display.flip()
        pygame.time.delay(10)
    
    if pygame.font:
        font = pygame.font.Font(None, 50)
        textgo = font.render("GAME OVER", 1, (255, 255, 255))
        textgopos = [width / 2 - 90, height / 2 - 10]
        print textgopos
        screen.blit(textgo, textgopos)
        pygame.display.flip()
    pygame.time.delay(2000)