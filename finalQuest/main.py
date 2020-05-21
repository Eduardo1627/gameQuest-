# This file was created by: Eduardo Noyola 

# Sources Cited:
    # Mr. Cozort's 4th period code walkthrough(utilized the code demonstrated as a template)
    # Utilizes Mr. Cozort's 2nd period code walkthrough(Took inspiration and ideas, and simple add-ons for my code)d
   
    # KidsCanCode Shmup Part 14: Game Over Screen 
    # https://www.youtube.com/watch?v=Z2K2Yttvr5g&t=46s

    # KidsCanCode Shump Part 11: Player Lives
    # https://www.youtube.com/watch?v=G5-4nV6LxgU&t=248s

    # KidsCanCode Shump Part 9: Shields
    # https://www.youtube.com/watch?v=vvgWfNLgK9c&t=399s


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

turret_image = pg.image.load(game_dir + "/img/turret.png")
# powerup_images['Health'] = pg.image.load(game_dir + "/img/health.png")
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
def show_go_screen():
    screen.blit(background_image,background_rect)
    draw_text(screen,"Space Crusders!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow Keys move, Space to fire", 22, WIDTH/ 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3/4 )
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP:
                waiting = False
def draw_health_bar(screen,x,y, pct):
    if pct <0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100 * BAR_LENGTH)
    outline_rect = pg.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x,y, fill, BAR_HEIGHT)
    pg.draw.rect(screen, GREEN, fill_rect)
    pg.draw.rect(screen,WHITE, outline_rect, 2)
def draw_ammo_bar(screen,x,y, pct):
    if pct <0:
        pct = 0
    if pct > 100 :
        pct = 100
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100 * BAR_LENGTH)
    outline_rect = pg.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x,y, fill, BAR_HEIGHT)
    pg.draw.rect(screen, YELLOW, fill_rect)
    pg.draw.rect(screen,WHITE, outline_rect, 2)
def draw_lives(screen,x,y, lives, img):
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
        # Speed of the player, hp of the player, and the total ammo of the player. In addition to the life. 
        self.speedx = 0
        self.speedy = 10
        self.hp = 100
        self.ammo = 100
        self.score = 0
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()

    # The Method "update" updates various things within the Player Class
    def update(self):
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
        if self.hp <= 0:
            self.hide()
            self.lives -= 1
            self.hp = 100
    # A method that creates lazer and the use of ammo within the game
    def pew(self):
        # If the ammo is greater than 0, the player can shoot lazers, but if its 0 then the shooting ability is disabled
        if self.ammo > 0:
            lazer1 = Lazer(self.rect.centerx, self.rect.top)
            lazer2 = Lazer(self.rect.right, self.rect.centery)
            lazer3 = Lazer(self.rect.left, self.rect.centery)
            all_sprites.add(lazer1)
            all_sprites.add(lazer2)
            all_sprites.add(lazer3)
            lazers.add(lazer1)
            lazers.add(lazer2)
            lazers.add(lazer3)
            self.ammo-=1
            # Makes sure that the ammo does not go over 100 
            if self.ammo > 100:
                self.ammo = 100
            # print(self.ammo
    def hide(self):
        self.hidden = True 
        self.hide_timer= pg.time.get_ticks()
        self.rect.center= (WIDTH / 2, HEIGHT + 200)


        
# The class that creates enemies 
class Mob(Sprite):
    #intiates class
    def __init__(self):
        #intiates Sprites 
        Sprite.__init__(self)
        # Dimensions of the mob 
        self.image = pg.transform.scale(mob_image, (40, 40))
        # Eliminates these colors 
        self.image.set_colorkey(BLACK)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH-self.rect.width)
        self.rect.y = random.randrange(0, 240)
        self.speedx = random.randrange(1,5)
        self.speedy = random.randrange(1,10)
        self.hp = 100
    def update(self):
        # Updates movement and bullets 
        self.rect.x += self.speedx
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speedx*=-1
            self.rect.y += 25
        if self.rect.y > HEIGHT:
            self.rect.y = -25
            self.rect.x = random.randrange(0, WIDTH-self.rect.width)
        self.shoot = random.randrange(1,1000)
        if self.shoot% 200 == 0:
            self.pew()
        # Kills the mobs and gives ammo to player plus increase the score 
        if self.hp <= 0: 
            self.kill()
            player.ammo += 5
            player.score += 2 


                
              
    # Creates lazers
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
        self.shoot = random.randrange(1,1000)
        if self.shoot % 150 == 0:
            self.pew()
        if self.hp <= 0: 
            self.kill()
            player.score += 10 
            player.ammo += 10
    # Shoots two lazers rather than one 
    def pew(self):
        antilazer1 = Antilazer(self.rect.left, self.rect.centery)
        antilazer2 = Antilazer(self.rect.right, self.rect.centery)
        all_sprites.add(antilazer1)
        all_sprites.add(antilazer2)
        antilazers.add(antilazer1)
        antilazers.add(antilazer2)

       








# the game loop
game_over = True 
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pg.sprite.Group()
        bosses = pg.sprite.Group()
        mobs = pg.sprite.Group()
        lazers = pg.sprite.Group()
        antilazers = pg.sprite.Group()
        player = pg.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(0,8):
            mob = Mob()
            all_sprites.add(mob)
            mobs.add(mob)

# spawns more mobs


 # where all the new things get created and grouped...
        
    clock.tick(FPS)

    for event in pg.event.get():
        # window x button
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.pew()
        


    

    # update
    all_sprites.update()
    
    for mob in mobs:
        shot = pg.sprite.spritecollide(mob, lazers, False)
        if shot: 
            mob.hp-= 5
            # print(mob.hp)
    for boss in bosses:
        shot1 = pg.sprite.spritecollide(boss,lazers,False)
        if shot1:
            boss.hp-=25
            # print(boss.hp)
    damaged = pg.sprite.spritecollide(player, antilazers, False)
    if damaged:
        player.hp -= 10 
    if player.lives == 0: 
        game_over = True

            
  

    hits = pg.sprite.spritecollide(player, antilazers, True)
    hits = pg.sprite.spritecollide(player, bosses, True)
    hits = pg.sprite.spritecollide(player, mobs, True)

    if hits:
        running = False
    
    if len(mobs) == 0:
        for i in range(0,8):
            mob = Mob()
            all_sprites.add(mob)
            mobs.add(mob)
        
    if len(bosses) == 0:
        if player.score % 20 == 0:
            boss = Boss()
            all_sprites.add(boss)
            bosses.add(boss)


    # creates the moving background 
    background_rect2.y = background_rect.y - 600
    background_rect.y+= player.speedy
    background_rect2.y+= player.speedy 

    if background_rect2.y >- 0:
        background_rect.y = background_rect.y - 600
    
    # Draw
    screen.fill(DARKBLUE)
    screen.blit(background_image, background_rect)
    screen.blit(background_image, background_rect2)
    draw_text(screen, str(player.score), 24, WIDTH / 2, 10)
    # draw_text(screen, str(Round), 24, WIDTH / 3, 10)
    draw_health_bar(screen,5,5,player.hp)
    draw_ammo_bar(screen,5,20,player.ammo)
    draw_lives(screen, WIDTH-100, 5, player.lives, player_mini)
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()