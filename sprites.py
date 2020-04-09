#
# Sprite classes for platform game
# © 2019 KidsCanCode LLC / All rights reserved.
# mr cozort planted a landmine by importing Sprite directly...
#Modules and imports pygame 
import time
import pygame as pg
from pygame.sprite import Sprite
from settings import *
vec = pg.math.Vector2

class Player(Sprite):
    # include game parameter to pass game class as argument in main...
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.hitpoints = 100

    def myMethod(self):
        #passes over the method 
        pass


    def jump(self):
        self.rect.x += 1
        #When the player jumps it "kills" or removes the platform 
        hits = pg.sprite.spritecollide(self, self.game.platforms, True)
        self.rect.x -= 1
        if hits: 
            #Height of the jump 
            self.vel.y = -15
        
    def update(self):
        #commands to move 
        self.acc = vec(0, 0.5)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
       # if keys[pg.K_w]:
           # self.acc.y = -PLAYER_ACC
        if keys[pg.K_s]:
            self.acc.y = PLAYER_ACC
        # ALERT - Mr. Cozort did this WAY differently than Mr. Bradfield...
        if keys[pg.K_SPACE]:
            self.jump()


        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # self.acc.y += self.vel.y * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y < 0:
            self.pos.y = HEIGHT
            self.canjump = False
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y <= HEIGHT :
            self.canjump = True
    
    
    

        self.rect.midbottom = self.pos
        
#created a healthbar and tied to player hp
# I added it ot the main.py under new, adn it won't change its width
# I think I need to add a blit to update the graphic 
class Platform(Sprite):
    #creates platforms 
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 5
    def blitme(self,x, y):
        #Blitz the screen 
        self.screen.blit(self.image, (x,y))
    def update(self):
        #Makes the platforms move
        self.rect.x += self.vx 
        if self.rect.x + self.rect.width > WIDTH or self.rect.x < 0:
            self.vx*= -1
class Healthbar(Sprite):
    #class to create a health bar, same thing as a bar 
    def __init__(self,game, x, y, w, h):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def blitme(self,x,y):
        # blitz the sceen to be able ot se
        self.game.screen.blit(self.image, (self.rect.x+WIDTH, self.rect.y))
    def update(self):
        #creates the health bar 
        self.rect.width = self.game.player.hitpoints 
        self.blitme(15, 15)
