import sys, pygame
from pygame.locals import *
from human import *
from fireball import *
from monster import *
from boss import *
from random import *
from level import *

def level2(size, screen):
    background = pygame.image.load('images/chalkboard lvl 2.png').convert_alpha()
    level2 = Level(size, screen, background)
    width = size[0]
    height = size[1]
    level2.maxHealth=1000
    level2.maxMana = 100
    
    #player animations
    move = (pygame.image.load('images/hero1walk.png').convert_alpha(), 4)
    attack = (pygame.image.load('images/hero1attack.png').convert_alpha(), 4, 3)
    defend = (pygame.image.load('images/hero1block.png').convert_alpha(), 1)
    defmov = (pygame.image.load('images/hero1blockwalk.png').convert_alpha(), 4)
    fire = (pygame.image.load('images/hero1magic.png').convert_alpha(), 19, 16)
    jump = (pygame.image.load('images/hero1jump.png').convert_alpha(), 10)
    fireball = pygame.image.load('images/fireball.gif').convert_alpha()
    
    #plus enemy animation
    plus = (pygame.image.load('images/pluswalk.png').convert_alpha(), 13)
    patk = (pygame.image.load('images/plusattack.png').convert_alpha(), 12, 9)
    level2.addEnemy((plus, patk), "Plus Sign", 30, 10, (0,0,0))
    
    #triangle enemy animations
    tri = (pygame.image.load('images/trianglewalk.png').convert_alpha(), 6)
    triatk = (pygame.image.load('images/triangleattack.png').convert_alpha(), 7, 6)
    level2.addEnemy((tri, triatk), "Triangle", 40, 15, (0,0,0))

    #fraction enemy animations
    frac = (pygame.image.load('images/fractionwalk.png').convert_alpha(), 8)
    level2.addEnemy((frac, patk), "Fraction", 20, 5, (0,0,0))

    #temp boss animations
    level2.addEnemy((plus, patk), "Plus Boss", 100, 20, (1000,1000,100))

    #items: potions, powerups?
    #potion = (pygame.image.load('images/health.gif').convert_alpha(), 1)
    #can anyone make a potion image for me?
    
    #player object
    #player1 = Human((move, attack, defend, defmov, fire, jump), fireball, 10, size)
    level2.makePlayer((move, attack, defend, defmov, fire, jump), fireball, 10, size)
    
    #save up some memory
    del move
    del attack
    del defend
    del defmov
    del fire
    del jump
    del fireball
    
    while level2.player1.health > 0:
        #level2.setEvents()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if (event.key == K_LEFT or event.key == K_RIGHT) and not level2.player1.special:
                    lastmov = level2.current_lr = event.key
                    if level2.player1.defending:
                        level2.player1.move(event.key)
                        level2.player1.defmov()
                    else:
                        level2.player1.walk(event.key)
                elif (event.key == K_UP or event.key == K_DOWN) and not level2.player1.special:
                    lastmov = level2.current_ud = event.key
                    if level2.player1.defending:
                        level2.player1.move(event.key)
                        level2.player1.defmov()
                    else:
                        level2.player1.walk(event.key)
                elif (event.key == K_f) and not level2.player1.special:
                    if level2.player1.mana > 19:
                        level2.player1.fire()
                elif event.key == K_SPACE and not level2.player1.special:
                    level2.player1.jump()
                elif event.key == K_p:
                    level2.spawnEnemy(0)
                elif (event.key == K_d) and not level2.player1.special:
                    if level2.player1.moving:
                        level2.player1.defmov()
                    else:
                        level2.player1.defend()
                elif (event.key == K_a) and not level2.player1.special:
                    level2.player1.attack()
                #elif (event.key == K_s) and not level2.player1.special:
                #    if level2.player1.mana > 44:
                #        level2.player1.magic_shield()
                elif event.key == K_BACKSPACE:
                    return 0
            
            elif event.type == pygame.KEYUP:
                if ((event.key == K_LEFT) or (event.key == K_RIGHT)
                   and (level2.current_lr == event.key)):
                    level2.player1.stop_lr()
                elif ((event.key == K_UP) or (event.key == K_DOWN)
                     and (level2.current_ud == event.key)):
                    level2.player1.stop_ud()
                elif event.key == K_d:
                    level2.player1.stop_defending()
                    if level2.player1.moving:
                        level2.player1.walk(lastmov)
                    
        level2.enemySetSpeed()
        level2.attackThings()
        if level2.end:
            return True
        level2.moveRight()
        level2.displayStuff()

    level2.gameOver()
    return False
