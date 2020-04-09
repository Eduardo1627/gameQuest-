#This file was created by: Eduardo Noyola 

#imports modules and pygame 
import pygame as pg
from pygame.sprite import Group
# from pg.sprite import Group
import random
import time
from settings import *
from sprites import *

class Game:
    #This class stores the game and all its functions 
    def __init__(self):
        # initialize game window, etc
        #creates the screen and makes the game run 
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
    

    def new(self):
        #creates the healthbar and platforms of the game and adds them into a group
        # start a new game
        self.all_sprites = Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.healthbar = Healthbar(self, 15, 15, self.player.hitpoints, 25)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.healthbar)
        ground = Platform(0, HEIGHT-40, WIDTH, 40)
        plat1 = Platform(200, 400, 150, 20)
        plat2 = Platform(150, 300, 150, 20)
        self.all_sprites.add(ground)
        self.platforms.add(ground)
        self.all_sprites.add(plat1)
        self.platforms.add(plat1)
        self.all_sprites.add(plat2)
        self.platforms.add(plat2)
        self.tempGroup = Group()
        #creates more platforms and makes sure they don't overlap 
        for plat in range(0,10):
            plat = Platform(random.randint(15, WIDTH-400), random.randint(200, HEIGHT), random.randint(50,100), 20)
            self.tempGroup.add(plat,ground)
            for current in self.tempGroup:
                #if player goes over the screen the platform dissapears 
                platHits = pg.sprite.spritecollide(plat, self.platforms, True)
                if platHits:
                    plat.kill()
                else:
                    #if there is not 10 then more will be added 
                    self.all_sprites.add(plat,ground)
                    self.platforms.add(plat,ground)
        

        # for plat in range(1,10):
        #     plat = Platform(random.randint(0, WIDTH), random.randint(0, HEIGHT), 200, 20)
        #     self.all_sprites.add(plat)
        #     self.platforms.add(plat)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        #If player hits the bottom of the platform they will suffer 10 hp damage 
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            if self.player.rect.top > hits[0].rect.top:
                print("i hit my head")
                print(self.healthbar.rect.width)
                self.player.vel.y = 10
                self.player.rect.top = hits[0].rect.bottom + 5
                self.player.hitpoints -= 10
                #If the player's health reaches 0, they die 
                if self.player.hitpoints == 0:
                    print("You are dead!")
                    self.player.kill()
                    time.sleep(2)
                    exit()
            # print("it collided")
            else:
                self.player.vel.y = 0
                self.player.pos.y = hits[0].rect.top+1

            

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False


    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()



    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass


#runs the game, in a while loop 
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
