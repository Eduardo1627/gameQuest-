#This file was created by Eduardo Noyola
#The code was sourced by Mr. Cozort's 4th period walkthrough class


#imports modules 
import pygame as pg
from pygame.sprite import Sprite
import random
from os import path

#Global variables 
WIDTH = 480
HEIGHT = 600
FPS = 60
score = 0

# define colors
WHITE = (255, 255, 255)
DARKBLUE = (39, 54, 77)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
game_dir = path.join(path.dirname(__file__))

# loads the images for the classes 
background_image = pg.image.load(game_dir + "/img/bg.png")
background_rect = background_image.get_rect()
background_rect2 = background_image.get_rect()
player_image = pg.image.load(game_dir + "/img/player.png")
mob_image = pg.image.load(game_dir + "/img/mob.png")

# initialize pygame
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Space Crusaders")
clock = pg.time.Clock()

#Creates an Arial font, so text can be included within the game, such as a text for how score 
font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#Player Class 
class Player(Sprite):
    #intiates the class
    def __init__(self):
        #intiates Sprite
        Sprite.__init__(self)
        #creates the image of the player
        self.image = pg.transform.scale(player_image, (50, 40))
        #removes all color black from the game
        self.image.set_colorkey(BLACK)
        #draws the player 
        self.rect = self.image.get_rect()
        #Places the player spawn point 
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        #different variables for the player 
        self.speedx = 0
        self.speedy = 10
        self.hitpoints = 100
        self.ammo = 100
    #A module that updates multiple things within the game 
    def update(self):
        #Assigns the value for the x speed 
        self.speedx = 0
        # self.speedy = 0
        #imports a library within pygame to allows for keys to be made 
        keystate = pg.key.get_pressed()
        # if keystate[pg.K_w]:
        #     self.pew()
        #the two different keys that will be used with the speed they add when the player moves
        if keystate[pg.K_a]:
            self.speedx = -8
        if keystate[pg.K_d]:
            self.speedx = 8
        # if keystate[pg.K_w]:
        #     self.speedy = -8
        # if keystate[pg.K_s]:
        #     self.speedy = 8
        #applies the speed to the player 
        self.rect.x += self.speedx
        # self.rect.y += self.speedy
    #this class creates the amount of lazers the player can shoot  
    def pew(self):
        #gives ammo the player 
        if self.ammo > 0:
            #if the ammo does not equal zero it keeps creating lazers 
            lazer = Lazer(self.rect.centerx, self.rect.top)
            all_sprites.add(lazer)
            lazers.add(lazer)
            self.ammo-=1
            # print(self.ammo)

#Class the creates mobs
class Mob(Sprite):
    #intializes the class
    def __init__(self):
        #intializes Sprite 
        Sprite.__init__(self)
        #creates the dimensions for the mobs 
        self.image = pg.transform.scale(mob_image, (20, 20))
        #deletes all the color black 
        self.image.set_colorkey(BLACK)
        #draws the mob 
        self.rect = self.image.get_rect()
        #gives the mobs random speeds and spawn points 
        self.rect.x = random.randrange(0, WIDTH-self.rect.width)
        self.rect.y = random.randrange(0, 240)
        self.speedx = random.randrange(1,10)
        self.speedy = random.randrange(1,10)
    #module that updates ceirtain functions within the game 
    def update(self):
        #gives the mobs the speed of x that is being given to them 
        self.rect.x += self.speedx
        #tracts the mobs and makes sure that they don't go farther than the width if not they will be redirected 
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speedx*=-1
            self.rect.y += 25
        if self.rect.y > HEIGHT:
            self.rect.y = -25
            self.rect.x = random.randrange(0, WIDTH-self.rect.width)

#This class creates the lazers 
class Lazer(Sprite):
    #intializes the class 
    def __init__(self, x, y):
        #intializes Sprite 
        Sprite.__init__(self)
        #gives the lazer dimensions 
        self.image = pg.Surface((5,25))
        #fills in the lazers shape into the color blue 
        self.image.fill(BLUE)
        #gives the lazer a shape 
        self.rect = self.image.get_rect()
        #gives the lazer a spawn point from where it will go(from the player)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Groups all the classes into an all_sprites group, so its more acessable 
all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
lazers = pg.sprite.Group()
player = Player()
all_sprites.add(player)
#Generates 8 enemies 
for i in range(0,8):
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)


# the game loop
running = True
while running: 
    # keep loop running based on clock
    clock.tick(FPS)
    for event in pg.event.get():
        # If the window x button is pressed the game ends or shuts off 
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.pew()

    # colliders that check if ceirtain groups have collided 
    all_sprites.update()
    hits = pg.sprite.groupcollide(mobs, lazers, True, True)

    hits = pg.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False
    
    #creates more mobs if they all die
    if len(mobs) == 0:
        for i in range(0,8):
            mob = Mob()
            all_sprites.add(mob)
            mobs.add(mob)

    #creates a moving background making it look like the players are moving quickly 
    background_rect2.y = background_rect.y-600
    background_rect.y += player.speedy
    background_rect2.y += player.speedy

    if background_rect2.y >- 0:
        background_rect.y = background_rect.y-600
    
    # Draws the text and the backgrounds 
    screen.fill(DARKBLUE)
    screen.blit(background_image, background_rect)
    screen.blit(background_image, background_rect2)
    draw_text(screen, str(score), 24, WIDTH / 2, 10)
    draw_text(screen, str(player.ammo), 24, WIDTH / 4, 10)
    all_sprites.draw(screen)
    pg.display.flip()

#shuts the game down
pg.quit()