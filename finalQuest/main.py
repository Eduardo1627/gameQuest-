#This file was created by Eduardo Noyola.
#Sources
#Mr. Cozort's walthrough within class

#Importing modules 
import pygame as pg
from pygame.sprite import Sprite 
import random 

#Global Variables 
WIDTH = 480
HEIGHT = 600
FPS = 60

#Color options
WHITE = (255, 255, 255)
DARKBLUE = (39,54,77)
BLACK = (0 ,0 ,0)
RED =(255, 0, 0)
GREEN = (0, 255,0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#Intializes game
pg.init()
pg.mixer.init( )
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Space Crusaders")
clock = pg.time.Clock()

#The Player class which creates the player and all its functions 
class Player(Sprite):
    #Intiates the class
    def __init__(self):
        #attributes for the player, but also decides where it will spawn in 
        Sprite.__init__(self)
        self.image = pg.Surface((50,40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10 
        self. speedx = 0 
        self.speedy = 0 
    #The update module, where the controls of the player are located in addition to its speed 
    def update(self):
        self.speedx = 0 
        self.speedy = 0 
        keystate = pg.key.get_pressed()
        if keystate[pg.K_a]:
            self.speedx = -8
        if keystate[pg.K_d]:
            self.speedx = 8
        if keystate[pg.K_w]:
            self.pew()
        # if keystate[pg.K_s]:
        #     self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
    #the module that creates the lazers 
    def pew(self):
        #where the lazer comes out from 
        lazer= Lazer(self.rect.centerx, self.rect.top)
        #adds the lazers into the sprites group no matter the number 
        all_sprites.add(lazer)
        lazers.add(lazer)
    def healthbar(self):
        pass 

#The class that creates the mobs similar to player 
class Mob(Sprite):
    #intiates the class 
    def __init__(self):
        #intiates sprite so it can be used 
       Sprite.__init__(self)
       #Gives the mobs its attributes and where it will spawn 
       self.image = pg.Surface((40,40))
       self.image.fill(YELLOW)
       self.rect = self.image.get_rect()
       self.rect.x = random.randrange(0, WIDTH-self.rect.width)
       self.rect.y = random.randrange(0, 240)
       self.speedx = random.randrange(1,10)
       self.speedy = random.randint(1,10)
       #the boundaries of the mobs 
       self.rect.x = 250
       self.rect.y = 250 
    #modules that contains the "controls" of the mob
    def update(self):
        #returns the mob back on the screen if it goes past the boundaries 
        self.rect.x += self.speedx
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speedx*= -1
            self.rect.y += 25
        if self.rect.y > HEIGHT:
            self.rect.y = -25
            self.rect.x = random.randrange( 0, WIDTH-self.rect.width)

#The lazer class which creates the lazers that the player shoots out 
class Lazer(Sprite):
    #intiates the class 
    def __init__(self,x,y):
        #intiates the sprite, so it can be used 
        Sprite.__init__(self)
        #gives the lazers all the attributes they will need 
        self.image = pg.Surface((5,25))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    #the module updates the lazers
    def update(self):
        #if the lazers are less than 0 then they will disappear 
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
     


#all the classes are placed within the sprites group 
all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
lazers = pg.sprite.Group()
player = Player()
lazer = Lazer(player.rect.x, player.rect.y)
all_sprites.add(lazer)
all_sprites.add(mobs)
all_sprites.add(player)
#a loop that generates more mobs and adds them to the sprites groups 
for i in range(0,30):
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)

#The game loop
running = True
while running: 
    #keeps loop running based on the clock
    clock.tick(FPS)
    for event in pg.event.get():
        # Window x button 
        if event.type == pg.QUIT:
            running = False 

    #updates all the sprites while the game is running 
    all_sprites.update()
    #if the lazers hit the mobs, then they will disappear 
    hits = pg.sprite.groupcollide(mobs, lazers, True, True)

    #if the mobs collide with the player, the player will die, thus ending the game 
    hits = pg.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False 

    #draw the screen 
    screen.fill(RED)
    all_sprites.draw(screen)
    pg.display.flip()
#closes the game 
pg.quit()
