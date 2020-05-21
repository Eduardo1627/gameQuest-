# This file was created by: Eduardo Noyola 
# Completed on May 20th of 2020 at 10:10pm


# Sources Cited:
    # Mr. Cozort's 4th period code walkthrough(utilized the code demonstrated as a template)

    # Utilizes Mr. Cozort's 2nd period code walkthrough(Took inspiration and ideas, and simple add-ons for my code)d
   
    # KidsCanCode Shmup Part 14: Game Over Screen 
    # https://www.youtube.com/watch?v=Z2K2Yttvr5g&t=46s

    # KidsCanCode Shump Part 11: Player Lives
    # https://www.youtube.com/watch?v=G5-4nV6LxgU&t=248s

    # KidsCanCode Shump Part 9: Shields
    # https://www.youtube.com/watch?v=vvgWfNLgK9c&t=399s

    # KidsCanCode Shump Part 12: Powerups 
    # https://www.youtube.com/watch?v=z6h6l1yJ5-w

    # KidsCanCode Shump Part 13: Powerups(Part 2)
    # https://www.youtube.com/watch?v=y2w-116htIQ&t=2s


# Imports modules
import pygame as pg
from pygame.sprite import Sprite 
import random 
from os import path 
import time 

# Global settings and variables
WIDTH = 480
HEIGHT = 600
FPS = 60
Round = 0 
POWERUP_TIME = 5000
POWERUP_TIME2 =  15000

# Defines all the colors 
WHITE = (255, 255, 255)
DARKBLUE = (39, 54, 77)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Creates a path between folders 
game_dir = path.join(path.dirname(__file__))

# Loads the background image
background_image = pg.image.load(game_dir + "/img/bg.png")
background_rect = background_image.get_rect()
background_rect2 = background_image.get_rect()

# Loads the player's image 
player_image = pg.image.load(game_dir + "/img/player.png")
player_mini = pg.transform.scale(player_image,(25,19))
player_mini.set_colorkey(BLACK)

# Loads the enemies' images 
mob_image = pg.image.load(game_dir + "/img/mob.png")
Boss_image = pg.image.load(game_dir + "/img/boss.png")

# Loads powerup images 
health_image= pg.image.load(game_dir + "/img/health.png")
ammo_image = pg.image.load(game_dir + "/img/ammo.png")
turret_image = pg.image.load(game_dir + "/img/turret.png")


# Initialize pygame
pg.init()
pg.mixer.init()

# Creates the screen 
screen = pg.display.set_mode((WIDTH, HEIGHT))
# The title of the game
pg.display.set_caption("Space Crusaders")
# Creates a timer 
clock = pg.time.Clock()

# Provides the font_name with the 'arial' font
font_name = pg.font.match_font('arial')

# Function allows text to be drawn within the screen 
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# Function creates the starting and ending screen 
def show_go_screen():
    # Creates the screen with the text
    screen.blit(background_image,background_rect)
    draw_text(screen,"Space Crusders!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow Keys move, Space to fire", 22, WIDTH/ 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3/4 )
    pg.display.flip()
    # Checks if the player wants to begin the game or play it again 
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP:
                waiting = False


# Function draws a health bar on the top left corner 
def draw_health_bar(screen,x,y, pct):
    # Makes sure the health does not continue going to left and it stays within the boundaries 
    if pct <0:
        pct = 0
    # Provides dimensiosn for the health bar 
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100 * BAR_LENGTH)
    outline_rect = pg.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x,y, fill, BAR_HEIGHT)
    pg.draw.rect(screen, GREEN, fill_rect)
    pg.draw.rect(screen,WHITE, outline_rect, 2)

# Functions draws a ammo bar on the top left corner 
def draw_ammo_bar(screen,x,y, pct):
    # Makes sure the bar remains within the borders of the outline 
    if pct <0:
        pct = 0
    if pct > 100 :
        pct = 100
    # Gives the bar its dimensions
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100 * BAR_LENGTH)
    outline_rect = pg.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x,y, fill, BAR_HEIGHT)
    pg.draw.rect(screen, YELLOW, fill_rect)
    pg.draw.rect(screen,WHITE, outline_rect, 2)

# Function draws the player's lives on the top right corner 
def draw_lives(screen,x,y, lives, img):
    # Checks how many lives there are and constanly draws them 
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i 
        img_rect.y = y
        screen.blit(img,img_rect)


# Player Class 
class Player(Sprite):
    # Intiates the class
    def __init__(self):
        # Intiates Sprite 
        Sprite.__init__(self)
        # Gives a scale for the player image
        self.image = pg.transform.scale(player_image, (60, 40))
        # Deletes all black within the image 
        self.image.set_colorkey(WHITE)
        # Places the image on the rectangle that makes up the player
        self.rect = self.image.get_rect()
        # Where the player spawns within the game 
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        # Player's attributes  
        self.speedx = 0
        self.speedy = 10
        self.hp = 100
        self.ammo = 100
        self.score = 0
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        self.power = 1
        self.power_timer = pg.time.get_ticks()
    # The Method "update" updates various things within the Player Class
    def update(self):
        # A timer that brings the player back to one gun or two turrets from two or three 
        if self.power > 2 and pg.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pg.time.get_ticks()
        if self.power > 1 and pg.time.get_ticks()- self.power_time > POWERUP_TIME2:
            self.power -= 1 
            self.power_time = pg.time.get_ticks() 
        # When the player loses a life, they disapper and there re-appear 
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx =WIDTH/ 2
            self.rect.bottom = HEIGHT-10
        # If no key is being pressed the player's speed will be zero and always returns to zero
        self.speedx = 0
        # Allows for keys to be assigned 
        keystate = pg.key.get_pressed()
        # Creates the keys that allow the player to move left and right 
        if keystate[pg.K_a]:
            self.speedx = -8
        if keystate[pg.K_d]:
            self.speedx = 8
        # Applies the speed to the player when the key is pressed 
        self.rect.x += self.speedx
        # If the player goes beyond the width, then will be returned or not allowed to go father 
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH 
        # This all applies for the left side 
        if self.rect.left < 0:
            self.rect.left = 0
        # If the player health reaches 0 multiple things happen 
        if self.hp <= 0:
            self.hide()
            self.lives -= 1
            self.hp = 100
            self.power = 1 
    # A method that creates lazer and the use of ammo within the game
    def pew(self):
        # If the ammo is greater than 0, the player can shoot lazers, but if its 0 then the shooting ability is disabled
        if self.ammo > 0:
            # The starting amount of turrets the player has 
            if self.power == 1:
                lazer1 = Lazer(self.rect.centerx, self.rect.top)
                all_sprites.add(lazer1)
                lazers.add(lazer1)
            # When one powerup is picked two turrets are given to the player 
            if self.power == 2:
                lazer2 = Lazer(self.rect.right, self.rect.centery)
                lazer3 = Lazer(self.rect.left, self.rect.centery)
                all_sprites.add(lazer2)
                all_sprites.add(lazer3)
                lazers.add(lazer2)
                lazers.add(lazer3)
            # When a second powerup is picked up before the second turret expires, a third is given 
            if self.power == 3:
                lazer1 = Lazer(self.rect.centerx, self.rect.top)
                all_sprites.add(lazer1)
                lazers.add(lazer1)
                lazer2 = Lazer(self.rect.right, self.rect.centery)
                lazer3 = Lazer(self.rect.left, self.rect.centery)
                all_sprites.add(lazer2)
                all_sprites.add(lazer3)
                lazers.add(lazer2)
                lazers.add(lazer3)
            # Everytime the player shoots one ammo is removed 
            self.ammo-=1
            # Makes sure that the ammo does not go over 100 
            if self.ammo > 100:
                self.ammo = 100
            # print(self.ammo)
    # Method that helps with hiding the player when it dies 
    def hide(self):
        self.hidden = True 
        self.hide_timer= pg.time.get_ticks()
        # Respawns the player
        self.rect.center= (WIDTH / 2, HEIGHT + 200)   
    # Method that allows for the powerups to increase and to be timed 
    def powerup(self):
        self.power += 1 
        self.power_time = pg.time.get_ticks()
        # Keeps the turrets from disappering 
        if self.power > 3:
            self.power = 3
            

# The class that creates enemies 
class Mob(Sprite):
    #intiates class
    def __init__(self):
        # Intiates Sprites 
        Sprite.__init__(self)
        # Dimensions of the mob 
        self.image = pg.transform.scale(mob_image, (40, 40))
        # Eliminates these colors 
        self.image.set_colorkey(BLACK)
        self.image.set_colorkey(WHITE)
        # Decides the spawn point and speed of the mob and gives it an image 
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH-self.rect.width)
        self.rect.y = random.randrange(0, 240)
        self.speedx = random.randrange(1,5)
        self.speedy = random.randrange(1,10)
        # health 
        self.hp = 50
    # Method updates multiple components 
    def update(self):
        # Updates movement and bullets 
        self.rect.x += self.speedx
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speedx*=-1
            self.rect.y += 25
        if self.rect.y > HEIGHT:
            self.rect.y = -25
            self.rect.x = random.randrange(0, WIDTH-self.rect.width)
        # Allows the mob to fire 
        self.shoot = random.randrange(1,1000)
        if self.shoot% 200 == 0:
            self.pew()
        # Kills the mob and gives the player a chance of getting a powerup or score 
        if self.hp <= 0: 
            self.kill()
            player.score += 2 
            # A 5% chance of the player getting HP powerup
            if random.random() > 0.95:
                hpPowerup = hpPow(self.rect.centerx, self.rect.bottom)
                all_sprites.add(hpPowerup)
                hpPowerups.add(hpPowerup)
            # A 15% chance of the player getting an AMMO powerup 
            if random.random() > 0.85:
                ammoPowerup = ammoPow(self.rect.centerx, self.rect.bottom)
                all_sprites.add(ammoPowerup)
                ammoPowerups.add(ammoPowerup)
            # A 2% chance of the player getting a TURRET powerup 
            if random.random() >0.95:
                turretPowerup = turretPow(self.rect.centerx, self.rect.bottom)
                all_sprites.add(turretPowerup)
                turretPowerups.add(turretPowerup)
    # Method creates the Mob's lazers 
    def pew(self):
        antilazer = Antilazer(self.rect.centerx, self.rect.bottom)
        all_sprites.add(antilazer)
        antilazers.add(antilazer)
        
# Lazer Class 
class Lazer(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        # Creates the lazer and applies a speed to it 
        self.image = pg.Surface((5,25))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        # Destroys the lazer so that the game wont lag 
        self.rect.y += self.speedy
        if self.rect.bottom <= 0:
            self.kill()

# Enemy Lazer Class
class Antilazer(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        # Gives the lazer a size and speed
        self.image = pg.Surface((5,25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 5
    
    def update(self):
        # Kills the lazers, so lag will not occur 
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

    
    def update(self):
        # Kills the lazers, so lag will not occur 
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
# Health powerup Class 
class hpPow(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        #Gives it its dimensions
        self.image = pg.transform.scale(health_image, (20, 20))
        # Eliminates these colors 
        self.image.set_colorkey(BLACK)
        #Gives the powerup speed
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 2.5
    
    def update(self):
        # Destroys the powerups so lag will not occur 
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill() 

class ammoPow(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        # Gives the powerup an image
        self.image = pg.transform.scale(ammo_image, (20, 20))
        # Eliminates these colors 
        self.image.set_colorkey(BLACK)
        #Gives the powerup a size and speed
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 2.5
    
    def update(self):
        # Destroys the powerup, so lag will not occur 
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill() 

# Class for the turret powerup 
class turretPow(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        # Gives the powerup an image 
        self.image = pg.transform.scale(turret_image, (20, 20))
        # Eliminates these colors 
        self.image.set_colorkey(BLACK)
        #Gives the powerup a size and speed
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 2.5
    # Method updates to destroy all powerups that go off the screen 
    def update(self):
        # Destroys powerups so lag will not occur 
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill() 

# Boss class 
class Boss(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # Gives it dimensions and a random speed and spawn point 
        self.image = pg.transform.scale(Boss_image, (80,80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH-self.rect.width)
        self.rect.y = random.randrange(0, 240)
        self.speedx = random.randrange(1,8)
        self.speedy = random.randrange(1,8)
        # Gives it hp 
        self.hp = 500
    def update(self):
       # Updates various compotents 
        self.rect.x += self.speedx
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speedx*=-1
            self.rect.y += 25
        if self.rect.y > HEIGHT:
            self.rect.y = -25
            self.rect.x = random.randrange(0, WIDTH-self.rect.width)
        # Allows the boss to randomly shoot 
        self.shoot = random.randrange(1,1000)
        if self.shoot % 150 == 0:
            self.pew()
        # When the bosses health reach 0 multiple things will happen 
        if self.hp <= 0: 
            # Kills the boss 
            self.kill()
            # Gives points 
            player.score += 10
            # 25% chance of getting a HP powerup 
            if random.random() > 0.75:
                hpPowerup = hpPow(self.rect.centerx, self.rect.bottom)
                all_sprites.add(hpPowerup)
                hpPowerups.add(hpPowerup)
            # 30% chance of getting an AMMO powerup 
            if random.random() > 0.70:
                ammoPowerup = ammoPow(self.rect.centerx, self.rect.bottom)
                all_sprites.add(ammoPowerup)
                ammoPowerups.add(ammoPowerup)
            # 22% Chance of getting a TURRET powerup 
            if random.random() >0.78:
                turretPowerup = turretPow(self.rect.centerx, self.rect.bottom)
                all_sprites.add(turretPowerup)
                turretPowerups.add(turretPowerup)
    # Method creates the bosses' lazers 
    def pew(self):
        # Creates two lazers rather than one 
        antilazer1 = Antilazer(self.rect.left, self.rect.centery)
        antilazer2 = Antilazer(self.rect.right, self.rect.centery)
        all_sprites.add(antilazer1)
        all_sprites.add(antilazer2)
        antilazers.add(antilazer1)
        antilazers.add(antilazer2)


# The game loop
game_over = True 
running = True
while running:
    # Allows for the end screen and starting screen to not have sprites until the player begins to play
    if game_over:
        # Where all things are created and grouped 
        show_go_screen()
        game_over = False
        all_sprites = pg.sprite.Group()
        hpPowerups = pg.sprite.Group()
        ammoPowerups = pg.sprite.Group()
        turretPowerups = pg.sprite.Group()
        bosses = pg.sprite.Group()
        mobs = pg.sprite.Group()
        lazers = pg.sprite.Group()
        antilazers = pg.sprite.Group()
        player = pg.sprite.Group()
        player = Player()
        all_sprites.add(player)
        # Spawns more mobs when they reach 0 
        for i in range(0,8):
            mob = Mob()
            all_sprites.add(mob)
            mobs.add(mob)
    
    # Keeps the game running at 60 frames per second 
    clock.tick(FPS)
    # Checks for these ceirtain events if they are occuring
    for event in pg.event.get():
        # Window x button
        if event.type == pg.QUIT:
            running = False
        # If the spacebar is pressed a lazer is shot by the player 
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.pew()
        
    # Updates all sprites while the game is running 
    all_sprites.update()
    
    # Checks all the mobs if they have been hit by a lazer
    for mob in mobs:
        # Checks if a lazer has hit a mob and if does it makes the lazer disappear 
        shot = pg.sprite.spritecollide(mob, lazers, True)
        # Everytime the mob is hit its hp lowers 
        if shot: 
            mob.hp-= 25
            # print(mob.hp)
    # Checks all the bosses if they have been hit by a lazer 
    for boss in bosses:
        # Checks if a lazer has hit a boss and if does it makes the lazer disappear 
        shot1 = pg.sprite.spritecollide(boss,lazers,True)
        # If the boss is shot it lower its hp 
        if shot1:
            boss.hp-= 50 
            # print(boss.hp)
    # Checks if the player has been hit by an antilazer, and if its true then the lazer disappears 
    damaged = pg.sprite.spritecollide(player, antilazers, True)
    # Lowers the player's health everytime its hit 
    if damaged:
        player.hp -= 10 
    # If the player's lives reach 0 the ending screen is shown 
    if player.lives == 0: 
        game_over = True
    # Checks if the player picks up the HP powerup and if it does it makes the powerup disappear
    hpBack = pg.sprite.spritecollide(player,hpPowerups, True)
    # If the player picks up the HP powerup the health is restored
    if hpBack:
        player.hp = 100
    # Checks if the player picks up an AMMO powerup and if it does it makes the powerup disappear 
    ammoBack= pg.sprite.spritecollide(player,ammoPowerups, True)
    # If the player picks up the AMMO powerup it gets 50 ammo back 
    if ammoBack:
        player.ammo += 50
    # Checks if the player picks up a TURRET powerup and if it does it makes the powerup disappear 
    turretBack = pg.sprite.spritecollide(player,turretPowerups, True)
    # If the player picks up the TURRET powerup, a turret is added 
    if turretBack:
        player.powerup()

    # Checks if the player collides with any of the enemies 
    hits = pg.sprite.spritecollide(player, bosses, True)
    hits = pg.sprite.spritecollide(player, mobs, True)
    # If the player collides it will lose a life and if it reaches 0 lives the game will end 
    if hits:
        player.lives -=1 
        if player.lives == 0:
            game_over = True 
    
    # Creates more mobs if there are 0 
    if len(mobs) == 0:
        for i in range(0,8):
            mob = Mob()
            all_sprites.add(mob)
            mobs.add(mob)

    # Creates more bosses if there are 0    
    if len(bosses) == 0:
        # Specifies when the boss can spawn im 
        if player.score % 20 == 0:
            boss = Boss()
            all_sprites.add(boss)
            bosses.add(boss)


    # Creates the moving background 
    background_rect2.y = background_rect.y - 600
    background_rect.y+= player.speedy
    background_rect2.y+= player.speedy 

    if background_rect2.y >- 0:
        background_rect.y = background_rect.y - 600
    
    # Draw's text and the bars, among other things
    screen.fill(DARKBLUE)
    screen.blit(background_image, background_rect)
    screen.blit(background_image, background_rect2)
    draw_text(screen, str(player.score), 24, WIDTH / 2, 10)
    draw_health_bar(screen,5,5,player.hp)
    draw_ammo_bar(screen,5,20,player.ammo)
    draw_lives(screen, WIDTH-100, 5, player.lives, player_mini)
    all_sprites.draw(screen)
    pg.display.flip()
# If x is pressed in windows, then the game stops 
pg.quit()