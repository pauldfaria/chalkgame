import sys, pygame
from pygame.locals import *
from human import *
from fireball import *
from monster import *
from boss import *
from random import *

class Level():
    def __init__(self, size, screen, background):
        self.width = size[0]
        self.height = size[1]
        self.size = size
        self.screen = screen
        self.setscreen = False
        self.end = False
        self.background = background
        self.font = pygame.font.Font(None, 36)

        #list of all things enemy
        self.enemyList = []
        self.curEnemies = []
        
        #used for creating enemies
        #self.boxx = False
        self.enemy = 0
        self.damage = 0
        self.bos = False
        #used so the boss isn't like a regular enemy

        #items: potions, powerups?
        self.itemm = False
        #potion = (pygame.image.load('images/health.gif').convert_alpha(), 1)
        # can anyone make a potion image for me?
        
        #sounds
        pygame.mixer.init(22050, -16, 2, 3072)
        
        self.offset = 0
        self.current_lr = self.current_ud = self.lastmov = "fubar"
        
        self.fireballs = []

    def makePlayer(self, animations, fireball, strength, size):
        self.player1 = Human(animations, fireball, strength, size)

    def addEnemy(self, animations, name, health, strength, drop):
        self.enemyList.append([animations, name, health, strength, drop])
        #print self.enemyList

    def spawnEnemy(self, number):
        blah = self.enemyList[number]
        tempo = Monster(blah[0], blah[1], blah[2], blah[3], blah[4], self.size)
        self.curEnemies.append(tempo)

    def spawnBoss(self):
        self.spawnEnemy(len(self.enemyList)-1)

    def enemySetSpeed(self):
        for box in self.curEnemies:
            box.refresh()
            #The box.move's borke something :(
            if (box.pos.right + box.pos.left) > (self.player1.pos.right + self.player1.pos.left):
                box.speed[0] = -1
                #box.move([-1, box.speed[1]])
            else:
                box.speed[0] = 1
                #box.move([1, box.speed[1]])
            if (box.pos.top + box.pos.bottom) < (self.player1.pos.top + self.player1.pos.bottom):
                box.speed[1] = 1
                #box.move([box.speed[0], 1])
            else:
                box.speed[1] = -1
                #box.move([box.speed[0], -1])
            if self.player1.touch(box):
                box.speed = [0, 0]

            if self.bos:
                box.speed = [0, 0]

    def attackThings(self):
        #if self.boxx:
        for box in self.curEnemies:
            if self.player1.touch(box):
                if self.player1.attacking and self.player1.animation.cur_frame == self.player1.damageframe and self.player1.counter % 5 == 0:
                    self.damage = self.player1.do_damage(box)
                    if box.health < 1:
                        #self.boxx = False
                        #if self.bos:
                        #    self.setscreen = False
                        #    self.end = True
                        #    return
                        self.bos = False
                        self.player1.health += box.drop[0]
                        if self.player1.health > self.maxHealth:
                            self.player1.health = self.maxHealth
                        self.player1.mana += box.drop[1]
                        if self.player1.mana > self.maxMana:
                            self.player1.mana = self.maxMana
                        self.player1.modifier += box.drop[2]
                        box.kill()
                        self.curEnemies.remove(box)
                        self.player1.kills += 1
                #if (not player1.defending) and box.attacking and box.animation.cur_frame == box.damageframe and box.counter % 5 == 0:
                if box.attacking and box.animation.cur_frame == box.damageframe and box.counter % 5 == 0:
                    if self.player1.defending:
                        box.modifier = 0.5
                    box.do_damage(self.player1)
                    if self.player1.health < 1:
                        self.player1.health = 0
                else:
                    box.attack()
            else:
                for fireball in self.fireballs:
                    if (box.touch(fireball)):
                        #don't want fireballs to kill bosses but still do massive
                        #damage to regular enemies
                        box.health -= 1
                        #fireball.kill()
                        if box.health < 1:
                            #self.boxx = False
                            if self.bos:
                                self.setscreen = False
                            self.bos = False
                            self.player1.health += box.drop[0]
                            if self.player1.health > self.maxHealth:
                                self.player1.health = self.maxHealth
                            self.player1.mana += box.drop[1]
                            if self.player1.mana > self.maxMana:
                                self.player1.mana = self.maxMana
                            self.player1.modifier += box.drop[2]
                            box.kill()
                            self.curEnemies.remove(box)
                            self.player1.kills += 1
                            fireball.kill()

    def moveRight(self):
        if self.player1.refresh():
            self.fireballs.append(Fireball(self.player1.fireball, self.player1.getfirepos(), self.width))
        if not self.setscreen and self.player1.pos.right >= (self.width * 5) / 7:
            self.offset -= 6
            self.player1.pos.right = (self.width * 5) / 7 - 1
            for box in self.curEnemies:
                if not self.bos:
                    box.speed[0] = -6
            if self.player1.kills != self.player1.kills % 10 == 0:
                if not self.bos:
                    self.spawnBoss()
                    self.curEnemies[len(self.curEnemies)-1].pos = self.curEnemies[len(self.curEnemies)-1].image.get_rect().move(self.width, self.height * 5 / 8)
                    #self.boxx = True
                    self.bos = True
                    self.setscreen = True
            elif randint(0,50) == 0:
                enemy = randint(0,2)
                self.spawnEnemy(enemy)
                    #removed cuz it sucks
                    #self.boxx image until we get an item class or w/e
                    #patk = (pygame.image.load('images/plusattack.png').convert_alpha(), 12, 9)
                    #self.curEnemies[0] = Monster((patk, patk), "Potion", 1, 0, (50,50,10), self.size)
                    #del patk #why not?
                    #the potion right now is a monster with 1 health and 0 strength
                    #might want to make an item class
                self.curEnemies[len(self.curEnemies)-1].move([self.width, randint(self.height * 5 / 8, self.height ) - 256])
                #doesn't want to spawn randomly
                #self.boxx = True
            for fireball in self.fireballs:
                fireball.change_speed((7,0))
        else:
            for fireball in self.fireballs:
                fireball.change_speed((14,0))
        
        if -self.offset > 2 * self.width:
            self.offset = 0

    #dunno how events work therefore this doesn't work
    def setEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if (event.key == K_LEFT or event.key == K_RIGHT) and not self.player1.special:
                    self.lastmov = self.current_lr = event.key
                    if self.player1.defending:
                        self.player1.move(event.key)
                        self.player1.defmov()
                    else:
                        self.player1.walk(event.key)
                elif (event.key == K_UP or event.key == K_DOWN) and not self.player1.special:
                    self.lastmov = self.current_ud = event.key
                    if self.player1.defending:
                        self.player1.move(event.key)
                        self.player1.defmov()
                    else:
                        self.player1.walk(event.key)
                elif (event.key == K_f) and not self.player1.special:
                    if self.player1.mana > 19:
                        self.player1.fire()
                elif event.key == K_SPACE and not self.player1.special:
                    self.player1.jump()
                elif (event.key == K_d) and not self.player1.special:
                    if self.player1.moving:
                        self.player1.defmov()
                    else:
                        self.player1.defend()
                elif (event.key == K_a) and not self.player1.special:
                    self.player1.attack()
                #elif (event.key == K_s) and not player1.special:
                #    if player1.mana > 44:
                #        player1.magic_shield()
                elif event.key == K_BACKSPACE:
                    return 0
            
            elif event.type == pygame.KEYUP:
                if ((event.key == K_LEFT) or (event.key == K_RIGHT)
                   and (self.current_lr == event.key)):
                    self.player1.stop_lr()
                elif ((event.key == K_UP) or (event.key == K_DOWN)
                     and (self.current_ud == event.key)):
                    self.player1.stop_ud()
                elif event.key == K_d:
                    self.player1.stop_defending()
                    if self.player1.moving:
                        self.player1.walk(self.lastmov)

    def displayStuff(self):
        self.screen.blit(self.background,(self.offset, 0))
        self.screen.blit(self.background,(self.offset + 2 * self.width, 0))
        
        if pygame.font:
            texthp = self.font.render("Health: %s" % self.player1.health, 1, (0, 255, 0))
            textmp = self.font.render("Mana: %s" % self.player1.mana, 1, (0, 0, 255))
            textkills = self.font.render("Kills: %s" % self.player1.kills, 1, (255, 0, 0))
            textposhp = [0, 0]
            textposmp = [0, 20]
            textposkills = [0, 40]
            self.screen.blit(texthp, textposhp)
            self.screen.blit(textmp, textposmp)
            self.screen.blit(textkills, textposkills)

            '''if self.boxx:
                enemyname = self.font.render("Enemy Name: " + self.curEnemies[0].name, 1, (255,255,255))
                enemyhp = self.font.render("Enemy Health: " + str(int(self.curEnemies[0].health)), 1, (255,0,0))
                damagetext = self.font.render(str(self.damage), 1, (255,0,0))
                damagetextpos = [self.curEnemies[0].pos[0]+128, self.curEnemies[0].pos[1]-128]
            else:
                enemyname = self.font.render("Enemy Name: Null", 1, (255,255,255))
                enemyhp = self.font.render("Enemy Health: Null", 1, (255,0,0))
                damagetext = self.font.render("", 1, (0,0,00))
                damagetextpos = [0, 0]
                self.damage = 0
            enemynamepos = [700, 0]
            enemyhppos = [700, 20]
            self.screen.blit(enemyname, enemynamepos)
            self.screen.blit(enemyhp, enemyhppos)
            self.screen.blit(damagetext, damagetextpos)'''
            #I'll figure out how to do this later
            #Maybe display in the corner the stats of the last enemy hit?
            #possibly display the damage/health for all enemies over their heads?

        for fireball in self.fireballs:
            fireball.refresh()
            self.screen.blit(fireball.image, fireball.pos)

        self.screen.blit(self.player1.image, self.player1.pos)
        for box in self.curEnemies:
            self.screen.blit(box.image, box.pos)

        pygame.display.flip()
        pygame.time.delay(5)

    def gameOver(self):
        pygame.mixer.music.load("sounds/failure.wav")
        pygame.mixer.music.play()
        if pygame.font:
            font = pygame.font.Font(None, 50)
            textgo = font.render("GAME OVER", 1, (255, 255, 255))
            textgopos = [self.width / 2 - 90, self.height / 2 - 10]
            self.screen.blit(textgo, textgopos)
        pygame.display.flip()
        pygame.time.delay(2000)
