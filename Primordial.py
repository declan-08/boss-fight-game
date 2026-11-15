# importing libraries needed for the game
# pygame is used for graphics and game functionality
# sys is used to allow the program to exit
# random is used for generating random attacks/positions
import pygame, sys
import random

# creating the game clock which controls frame rate
mainClock= pygame.time.Clock()

# initialising pygame
pygame.init()

# creating the main game window with a fixed resolution
screen = pygame.display.set_mode((1366,768))

# creating fonts that will be used for titles and buttons in the UI
title_font = pygame.font.SysFont("Castellar",60)
button_font = pygame.font.SysFont("Bell MT",30)

# function used to draw text to the screen at a given position
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))

# this function creates a larger rectangle around a sprite
# it is mainly used for interaction zones such as attacking or interacting with objects
def interaction_rect(sprite, distance):
    return sprite.rect.inflate(distance * 2, distance  * 2)

# class representing the boss enemy "Vulcan"
class Vulcan(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        # boolean to check if the boss is currently exhausted
        self.exhausted = False
        #health value for the boss
        self.health = 15
        # iframe = invincibility frames so the boss cannot be hit repeatedly instantly
        self.iframe = 500
        # keeps track of when the boss was last hit
        self.last_hit = 0
        # timer that determines how often the boss becomes exhausted
        self.exhaustiontimer = 10000
        # time since last exhaustion state
        self.lastexhaustion = 0
        # how long the exhaustion state lasts
        self.duration = 5000
        # stores when the exhaustion state began
        self.exhaustion_start = 0
        # boolean to track if the boss has died
        self.death = False
        # loading and scaling the boss sprite image
        self.image = pygame.transform.scale(pygame.image.load("Vulcan.png"), (500,514))
        # creating the rectangle used for position and collision
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]
    
    # function that manages the boss exhaustion mechanic
    def exhaustion(self):
        global attacks
        # getting the current time in milliseconds
        self.current_time = pygame.time.get_ticks()
        # if the boss is not exhausted and the exhaustion timer has passed
        if self.exhausted == False and self.current_time-self.lastexhaustion>=self.exhaustiontimer:
            
            # boss becomes exhausted and attacks stop
            self.exhausted = True
            damage_sprites.empty()
            attacks.selectedattack = []
            # storing when the exhaustion started
            self.exhaustion_start = self.current_time
            # changing the boss sprite to an exhausted version
            self.image = pygame.transform.scale(pygame.image.load("vulcanexhausted_enhanced.png"), (500,514))
            self.rect = self.image.get_rect(topleft=(375,25))
        
        # once the exhaustion duration has passed the boss returns to normal
        if self.exhausted == True and self.current_time - self.exhaustion_start >= self.duration:
            self.exhausted = False
            # restarting the attack system
            attacks = Attacks()
            damage_sprites.add(attacks)
            # resetting exhaustion timer
            self.lastexhaustion = self.current_time
            # restoring the normal boss sprite
            self.image = pygame.transform.scale(pygame.image.load("Vulcan.png"), (500,514))
            self.rect = self.image.get_rect(topleft=(375,35))
        
        # if the boss health reaches zero the boss dies
        if vulcan.health <= 0:
            self.death = True
        

# class used to create explosion animations in the game
class Detonation(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        # boolean used to check if the explosion animation should currently play
        self.explosion = False
        # list storing all frames of the explosion animation
        self.explosionsprites = []
        # loading each frame of the explosion animation
        self.explosionsprites.append(pygame.image.load("transparent.png"))
        self.explosionsprites.append(pygame.image.load("explosion-d1.png"))
        self.explosionsprites.append(pygame.image.load("explosion-d2.png"))
        self.explosionsprites.append(pygame.image.load("explosion-d3.png"))
        self.explosionsprites.append(pygame.image.load("explosion-d4.png"))
        self.explosionsprites.append(pygame.image.load("explosion-d5.png"))
        self.explosionsprites.append(pygame.image.load("explosion-d6.png"))
        self.explosionsprites.append(pygame.image.load("explosion-d7.png"))
        self.explosionsprites.append(pygame.image.load("explosion-d8.png"))
        self.explosionsprites.append(pygame.image.load("explosion-d9.png"))
        self.explosionsprites.append(pygame.image.load("explosion-d10.png"))
        self.explosionsprites.append(pygame.image.load("explosion-d11.png"))
        self.explosionsprites.append(pygame.image.load("explosion-d12.png"))
        # keeps track of which frame of the explosion animation is currently displayed
        self.current_explosionsprite = 0
        # scaling every frame to the correct size
        for x in range(0,len(self.explosionsprites)):
            self.explosionsprites[x]=pygame.transform.scale(self.explosionsprites[x],(225,225))
        # setting the initial image
        self.image = self.explosionsprites[int(self.current_explosionsprite)]
        # creating the rectangle used for positioning
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]

    # function used to activate the explosion animation    
    def activateexplosion(self):
            self.explosion = True
    # function that updates the explosion animation frame each game tick    
    def updateexplosion(self):
        if self.explosion == True:
            # slowly increasing frame index to animate explosion
            self.current_explosionsprite += 0.125
            # if animation reaches the end it resets and stops
            if self.current_explosionsprite>=len(self.explosionsprites):
                self.current_explosionsprite = 0
                self.explosion = False
            # updating displayed sprite        
            self.image = self.explosionsprites[int(self.current_explosionsprite)]


# class representing the altar object that the player can interact with
class Altar(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        # boolean used to track if the altar has already been used
        self.used = False
        # list storing altar animation frames
        self.sprites = []
        # loading altar images
        self.sprites.append(pygame.image.load("Altar0.png"))
        self.sprites.append(pygame.image.load("Altar1.png"))
        self.sprites.append(pygame.image.load("Altar2.png"))
        self.sprites.append(pygame.image.load("Altar3.png"))
        # current frame of the altar animation
        self.current_sprite = 0
        # scaling altar images
        for x in range(0,len(self.sprites)):
            self.sprites[x]=pygame.transform.scale(self.sprites[x],(225,225))
        # setting initial image
        self.image = self.sprites[self.current_sprite]

        # creating rectangle for collision and positioning
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]
    
    # animation update for the altar
    def update(self):
        # cycles through animation frames
        self.current_sprite += 0.125
        # if the animation reaches the end it loops back
        if self.current_sprite>=len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
    
    # function called when the player interacts with the altar
    def interact(self):
        # ensures the altar can only be used once
        if self.used == False:
            # removing altar from moving sprite group
            moving_sprites.remove(altar)
            # marking altar as used
            self.used = True

# class representing the player character
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        # storing player starting position
        self.pos_x = pos_x
        self.pos_y = pos_y
        # lists that store animation frames for different player states
        self.attacksprites = []
        # booleans used to determine what animation should play
        self.is_animatingwalk = False
        self.is_animatingattack = False
        self.is_animatingidle = True
        # booleans used for directional movement
        self.upwards = False
        self.right = False
        self.left = False
        self.downwards = False
        # loading player attack animation frames
        self.attacksprites.append(pygame.image.load("cultist_priest_attack_1.png"))
        self.attacksprites.append(pygame.image.load("cultist_priest_attack_2.png"))
        self.attacksprites.append(pygame.image.load("cultist_priest_attack_3.png"))
        self.attacksprites.append(pygame.image.load("cultist_priest_attack_4.png"))
        self.attacksprites.append(pygame.image.load("cultist_priest_attack_5.png"))
        # variable used to track attack animation frame
        self.current_attacksprite = 0
        # scaling attack frames
        for x in range(0,len(self.attacksprites)):
            self.attacksprites[x]=pygame.transform.scale(self.attacksprites[x],(150,225))
        # setting the image and rectangle
        self.image = self.attacksprites[self.current_attacksprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x,self.pos_y]

        # creating list for idle animation frames
        self.idlesprites = []
        # loading player idle animation frames
        self.idlesprites.append(pygame.image.load("cultist_priest_idle_1.png"))
        self.idlesprites.append(pygame.image.load("cultist_priest_idle_2.png"))
        self.idlesprites.append(pygame.image.load("cultist_priest_idle_3.png"))
        self.idlesprites.append(pygame.image.load("cultist_priest_idle_4.png"))
        self.idlesprites.append(pygame.image.load("cultist_priest_idle_5.png"))
        # variable used to track idle animation frame
        self.current_idlesprite = 0
        # scaling idle frames
        for x in range(0,len(self.idlesprites)):
            self.idlesprites[x]=pygame.transform.scale(self.idlesprites[x],(150,225))
        # setting the image and rectangle
        self.image = self.idlesprites[self.current_idlesprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x,self.pos_y]
        # creating list for walking animation frames
        self.walksprites = []
        # loading player walking animation frames
        self.walksprites.append(pygame.image.load("cultist_priest_walk_1.png"))
        self.walksprites.append(pygame.image.load("cultist_priest_walk_2.png"))
        self.walksprites.append(pygame.image.load("cultist_priest_walk_3.png"))
        self.walksprites.append(pygame.image.load("cultist_priest_walk_4.png"))
        self.walksprites.append(pygame.image.load("cultist_priest_walk_5.png"))
        self.walksprites.append(pygame.image.load("cultist_priest_walk_6.png"))
        # variable used to track walking animation frame
        self.current_walksprite = 0
        # scaling walking frames
        for x in range(0,len(self.walksprites)):
            self.walksprites[x]=pygame.transform.scale(self.walksprites[x],(150,225))
        # setting the image and rectangle
        self.image = self.walksprites[self.current_walksprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x,self.pos_y]

    # function used to trigger the attack animation    
    def animateattack(self):
        self.is_animatingattack = True
    # updates the attack animation each frame
    def updateattack(self):
        if self.is_animatingattack == True:
            # disabling other animations while attacking
            self.is_animatingidle = False
            self.is_animatingwalk = False
            # progressing through the attack animation frames
            self.current_attacksprite += 0.125
            # if the animation reaches the final frame it resets
            if self.current_attacksprite>=len(self.attacksprites):
                self.current_attacksprite = 0
                self.is_animatingattack = False
                self.is_animatingidle = True
            # updating the sprite image
            self.image = self.attacksprites[int(self.current_attacksprite)]
    
    # updates idle animation when the player is not moving
    def updateidle(self):
            if self.is_animatingidle == True:
                # progressing idle animation frames
                self.current_idlesprite += 0.125
                # looping animation back to the start
                if self.current_idlesprite>=len(self.idlesprites):
                    self.current_idlesprite = 0
                self.image = self.idlesprites[int(self.current_idlesprite)]
    
    # function used to start the walking animation
    def animatewalk(self):
        self.is_animatingwalk = True
    # updates the walking animation frames
    def updatewalk(self):
        if self.is_animatingwalk == True:
            # disabling idle animation while walking
            self.is_animatingidle = False
            # progressing through walking frames
            self.current_walksprite += 0.125
            # resetting animation once it reaches the end
            if self.current_walksprite>=len(self.walksprites):
                self.current_walksprite = 0
                self.is_animatingwalk = False
                self.is_animatingidle = True
            # updating sprite image
            self.image = self.walksprites[int(self.current_walksprite)]
    
    # sets movement flag when the up key is pressed
    def upkey(self):
        self.upwards = True
    # sets movement flag when the right key is pressed
    def rightkey(self):
        self.right = True
    # sets movement flag when the left key is pressed
    def leftkey(self):
        self.left = True
    # sets movement flag when the down key is pressed
    def downkey(self):
        self.downwards = True
    # function that handles the player's movement and boundary limits
    def movement(self):
        # moving player upwards
        if self.upwards == True:
            self.rect.y-=5
            self.upwards = False
        # moving player right
        if self.right == True:
            self.rect.x+=5
            self.right = False
        # moving player left
        if self.left == True:
            self.rect.x-=5
            self.left = False
        # moving player down
        if self.downwards == True:
            self.rect.y+=5
            self.downwards = False
        # preventing the player from leaving the left side of the screen
        if self.rect.x<=0:
            self.rect.x=0
        # preventing the player from leaving the right side of the screen
        if self.rect.x>=1216:
            self.rect.x=1216
        # preventing the player from leaving the bottom of the screen
        if self.rect.y>=543:
            self.rect.y=543
        # preventing the player from leaving the top of the screen
        if self.rect.y<=0:
            self.rect.y=0
        

# variable used to check if the mouse has been clicked
click = False

# function that controls the main menu screen
def main_menu():
    global click
    # infinite loop so the menu continues running until a button is pressed
    while True:
        # setting the window title
        pygame.display.set_caption("Main Menu")
        # filling the background with a dark colour
        screen.fill((58,55,58))
        # drawing the game title text
        draw_text("Primordial",title_font, (37, 35, 33),475,175) 
        # getting the current mouse position
        mx, my = pygame.mouse.get_pos()

        # creating rectangles that act as buttons
        start_button = pygame.Rect((615,275, 150, 100))
        postgame_button = pygame.Rect((615, 475, 150, 100))
        # checking if the mouse is hovering over the start button
        if start_button.collidepoint((mx,my)):
            if click == True:
                maingame()
        # checking if the mouse is hovering over the postgame button
        if postgame_button.collidepoint((mx,my)):
            if click == True:
                postgame()
        # drawing the buttons
        pygame.draw.rect(screen, (253, 101, 45), start_button)
        pygame.draw.rect(screen, (253, 101, 45), postgame_button)

        # rendering button text
        text_surface = button_font.render("Start", True, (37, 35, 33 ))
        text_rect = text_surface.get_rect(center=start_button.center)
        screen.blit(text_surface, text_rect)
        
        text_surface2 = button_font.render("Post-Game", True, (37, 35, 33 ))
        text_rect2 = text_surface2.get_rect(center=postgame_button.center)
        screen.blit(text_surface2, text_rect2)
        
        # resetting click variable each frame
        click = False

        # handling events such as quitting or mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # detecting left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            # allowing player to exit using escape key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        mainClock.tick(60)

# loading the floor background image and scaling it to the window
background = pygame.image.load("floor_tiles_custom.png").convert()
background = pygame.transform.scale(background, (1366,768))
# loading grass textures used in the arena decoration
grass = pygame.image.load("grass.png").convert_alpha()
grass = pygame.transform.scale(grass, (150,150))
grass2 = pygame.transform.scale(grass, (100,100))
grass3 = pygame.transform.scale(grass, (75,75))
# sprite groups used to organise different types of game objects
moving_sprites = pygame.sprite.Group()
misc_sprites = pygame.sprite.Group()
dragon_sprites = pygame.sprite.Group()
damage_sprites = pygame.sprite.Group()

# creating the player object
player = Player(575,600)

# class used for the vertical fire column attack
class FireColumn(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        # list storing animation frames for the fire column
        self.frames = []
        # first few frames are telegraph frames which warn the player
        self.frames.append(pygame.image.load("column_telegraph.jpg"))
        self.frames.append(pygame.image.load("column_telegraph.jpg"))
        self.frames.append(pygame.image.load("column_telegraph.jpg"))
        self.frames.append(pygame.image.load("column_telegraph.jpg"))
        self.frames.append(pygame.image.load("column_telegraph.jpg"))
        self.frames.append(pygame.image.load("column_telegraph.jpg"))
        # remaining frames are the actual fire column animation
        self.frames.append(pygame.image.load("fire_column_medium_1.png"))
        self.frames.append(pygame.image.load("fire_column_medium_2.png"))
        self.frames.append(pygame.image.load("fire_column_medium_3.png"))
        self.frames.append(pygame.image.load("fire_column_medium_4.png"))
        self.frames.append(pygame.image.load("fire_column_medium_5.png"))
        self.frames.append(pygame.image.load("fire_column_medium_6.png"))
        self.frames.append(pygame.image.load("fire_column_medium_7.png"))
        self.frames.append(pygame.image.load("fire_column_medium_8.png"))
        self.frames.append(pygame.image.load("fire_column_medium_9.png"))
        self.frames.append(pygame.image.load("fire_column_medium_10.png"))
        self.frames.append(pygame.image.load("fire_column_medium_11.png"))
        self.frames.append(pygame.image.load("fire_column_medium_12.png"))
        self.frames.append(pygame.image.load("fire_column_medium_13.png"))
        self.frames.append(pygame.image.load("fire_column_medium_14.png"))

        # scaling frames so the column spans the arena vertically
        for x in range(0,len(self.frames)):
            self.frames[x] = pygame.transform.scale(self.frames[x],(150,768))
        # setting position
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(pos_x,pos_y))
    # updating animation frame each tick
    def update(self):
        self.current_frame+=0.125
        # if animation finishes the sprite removes itself
        if self.current_frame>=len(self.frames):
            self.kill()
            return

        self.image = self.frames[int(self.current_frame)]

# class responsible for controlling boss attacks
class Attacks(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # variable storing which dragon/boss is currently active
        self.current_dragon = 0
        # cooldown timers controlling how often attacks spawn
        self.spawn_cooldown = 2000
        self.column_cooldown = 4000
        self.last_spawn = 0
        self.last_columnspawn = 0
        # creating an empty column attack
        self.column = FireColumn(-1000,-1000)
        # variable storing the currently selected attack
        self.selectedattack = []
        # lists storing different attack animations
        self.vulcanattack1 = []
        self.vulcanattack1.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack1.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack1.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack1.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack1.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack1.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack1.append(pygame.image.load("explosion-b1.png"))
        self.vulcanattack1.append(pygame.image.load("explosion-b2.png"))
        self.vulcanattack1.append(pygame.image.load("explosion-b3.png"))
        self.vulcanattack1.append(pygame.image.load("explosion-b4.png"))
        self.vulcanattack1.append(pygame.image.load("explosion-b5.png"))
        self.vulcanattack1.append(pygame.image.load("explosion-b6.png"))
        self.vulcanattack1.append(pygame.image.load("explosion-b7.png"))
        self.vulcanattack1.append(pygame.image.load("explosion-b8.png"))
        self.vulcanattack1.append(pygame.image.load("explosion-b9.png"))
        self.vulcanattack1.append(pygame.image.load("explosion-b10.png"))
        self.vulcanattack1.append(pygame.image.load("explosion-b11.png"))
        self.vulcanattack1.append(pygame.image.load("explosion-b12.png"))
        
        self.vulcanattack2 = []
        self.vulcanattack2.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack2.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack2.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack2.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack2.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack2.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack2.append(pygame.image.load("explosion-f1.png"))
        self.vulcanattack2.append(pygame.image.load("explosion-f2.png"))
        self.vulcanattack2.append(pygame.image.load("explosion-f3.png"))
        self.vulcanattack2.append(pygame.image.load("explosion-f4.png"))
        self.vulcanattack2.append(pygame.image.load("explosion-f5.png"))
        self.vulcanattack2.append(pygame.image.load("explosion-f6.png"))
        self.vulcanattack2.append(pygame.image.load("explosion-f7.png"))
        self.vulcanattack2.append(pygame.image.load("explosion-f8.png"))

        self.vulcanattack3 = []
        self.vulcanattack3.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack3.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack3.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack3.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack3.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack3.append(pygame.image.load("attack_telegraph.png"))
        self.vulcanattack3.append(pygame.image.load("splosion 1.png"))
        self.vulcanattack3.append(pygame.image.load("splosion 2.png"))
        self.vulcanattack3.append(pygame.image.load("splosion 3.png"))
        self.vulcanattack3.append(pygame.image.load("splosion 4.png"))

        self.image = pygame.image.load("transparent.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [0,0]
        # storing all possible attacks in one list
        self.vulcanattacks = [self.vulcanattack1,self.vulcanattack2,self.vulcanattack3]
        # scaling all attack frames
        for x in range (0,len(self.vulcanattacks)):
            for y in range (0,len(self.vulcanattacks[x])):
                self.vulcanattacks[x][y] = pygame.transform.scale(self.vulcanattacks[x][y],(150,225))
        self.currentattacksprite = 0
        # if the active boss is Vulcan an attack is selected
        if self.current_dragon == "vulcan":
            self.selectedattack = self.vulcanattacks[random.randint(0,2)]
            self.image = self.selectedattack[self.currentattacksprite]
            self.rect = self.image.get_rect()
            self.rect.topleft = [random.randint(player.rect.x-100,player.rect.x+100),random.randint(player.rect.y-100,player.rect.y+100)]

    # function updating boss attack behaviour       
    def attackupdate(self):
        # if no dragon is active the function exits
        if self.current_dragon == 0:
            return
       
        self.current_time = pygame.time.get_ticks()
        # spawning fire columns periodically
        if self.current_time - self.last_columnspawn > self.column_cooldown:
            for x in range(0,3):
                self.column = FireColumn(100+(x*500),100)
                damage_sprites.add(self.column)
                self.column = FireColumn(100+(x*500),0)
                damage_sprites.add(self.column)

            self.last_columnspawn = self.current_time
            return
        # if no attack is currently active a new one is selected
        if not self.selectedattack:
            if self.current_time - self.last_spawn > self.spawn_cooldown:
                self.selectedattack = random.choice(self.vulcanattacks)
                self.currentattacksprite = 0
                self.image = self.selectedattack[0]
                self.rect = self.image.get_rect()
                self.rect.topleft = [random.randint(player.rect.x-100,player.rect.x+100),random.randint(player.rect.y-100,player.rect.y+100)]
                self.last_spawn = self.current_time
            return
        # progressing the attack animation
        self.currentattacksprite += 0.125
        # once animation ends the attack resets
        if self.currentattacksprite >= len(self.selectedattack):
            self.selectedattack = []
            self.image = pygame.image.load("transparent.png")
            return
        # updating the image to the correct attack animation frame
        self.image = self.selectedattack[int(self.currentattacksprite)]



# creating the main attack controller object
attacks = Attacks()
# creating the altar object that the player interacts with to start the boss fight
altar = Altar(575,180)
# creating the explosion animation that plays when the altar is activated
explosion = Detonation(575,180)
# adding the altar to the moving sprite group so it is drawn and updated
moving_sprites.add(altar)
# sprite group used to store the player
player_sprite = pygame.sprite.Group()
# adding the player to its sprite group
player_sprite.add(player)
# adding the explosion sprite to the moving sprites group
moving_sprites.add(explosion)

# class responsible for displaying and updating the player's health
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        # iframe used to prevent the player taking damage multiple times instantly
        self.iframe = 1300
        # storing the time the player was last hit
        self.last_hit = 0
        # boolean used to check if the player has died
        self.death = False
        # list storing different health bar images
        self.healthsprites = []
        # each image represents a different health state
        self.healthsprites.append(pygame.transform.scale(pygame.image.load("heart_row_1.png"),(100,100)))
        self.healthsprites.append(pygame.transform.scale(pygame.image.load("heart_row_3.png"), (100,100)))
        self.healthsprites.append(pygame.transform.scale(pygame.image.load("heart_row_5.png"), (100,100)))
        self.healthsprites.append(pygame.transform.scale(pygame.image.load("heart_row_7.png"), (100,100)))
        # starting health state
        self.currenthealthsprite = 0
        self.image = self.healthsprites[self.currenthealthsprite]
        # setting the position of the health bar on screen
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]
    # function used to update the player's health based on collisions
    def update(self):
        # getting the current game time
        self.current_time = pygame.time.get_ticks()
        # checking if the player is hit by the boss attack animation
        if pygame.sprite.spritecollide(attacks,player_sprite,dokill=False) and attacks.currentattacksprite>=6 and self.current_time-self.last_hit>=self.iframe:
            self.currenthealthsprite+=1
            self.last_hit = self.current_time
        # checking collisions with fire column attacks
        for sprite in damage_sprites:
            if isinstance(sprite, FireColumn):
                if sprite.rect.colliderect(player.rect) and sprite.current_frame >= 6:
                    if self.current_time - self.last_hit >= self.iframe:
                        self.currenthealthsprite += 1
                        self.last_hit = self.current_time
        # if health reaches the final sprite the player dies
        if self.currenthealthsprite>=len(self.healthsprites):
                self.currenthealthsprite = 0
                self.death = True
        # updating the health bar image
        self.image = self.healthsprites[self.currenthealthsprite]

        

# creating the health bar object
healthbar = HealthBar(1150,75)
# adding the health bar to miscellaneous sprite group
misc_sprites.add(healthbar)
# creating the boss object
vulcan = Vulcan(375,25)
# adding the boss to the dragon sprite group
dragon_sprites.add(vulcan)
# adding attack controller to damage sprites
damage_sprites.add(attacks)
# loading the death screen background
deathbackground = pygame.transform.scale(pygame.image.load("you_died_screen.png"),(1366,768)).convert()
# loading the victory screen background
victorybackground = pygame.transform.scale(pygame.image.load("victory_screen.png"),(1366,768)).convert()

# function that runs the death screen
def death_screen():
    while True:
        # setting the window title
        pygame.display.set_caption("You Died")
        # displaying the death screen background
        screen.blit(deathbackground,(0,0))
        # checking for user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # pressing enter restarts the main game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    maingame()
                # pressing escape returns to the main menu
                if event.key == pygame.K_ESCAPE:
                    main_menu()
        
        pygame.display.update()
        mainClock.tick(60)
# function that runs the victory screen
def victory_screen():
    while True:
        pygame.display.set_caption("Congratulations!")
        # displaying victory background
        screen.blit(victorybackground,(0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # pressing enter returns to the main menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main_menu()
        
        pygame.display.update()
        mainClock.tick(60)

# main gameplay loop
def maingame():
    global attacks
    global vulcan
    running = True
    # boolean used to determine whether decorative grass is displayed
    show_grass = True
    while running:
        # drawing the arena background
        screen.blit(background, (0, 0))
        pygame.display.set_caption("Main Game")
        # drawing decorative grass tiles in the arena
        if show_grass == True:
            # these grass sprites visually decorate the altar
            screen.blit(background,(0,0))
            screen.blit(grass, (625,225))
            screen.blit(grass2, (625,225))
            screen.blit(grass, (650,250))
            screen.blit(grass2, (650,250))
            screen.blit(grass,(700,350))
            screen.blit(grass2,(700,350))
            screen.blit(grass,(715,230))
            screen.blit(grass2,(715,230))
            screen.blit(grass,(600,325))
            screen.blit(grass2,(600,325))
            screen.blit(grass2,(650,350))
            screen.blit(grass2,(680,375))
            screen.blit(grass,(535,350))
            screen.blit(grass2,(535,350))
            screen.blit(grass,(500,275))
            screen.blit(grass2,(500,275))
            screen.blit(grass2,(525,250))
            screen.blit(grass2,(550,275))
            screen.blit(grass,(600,225)) 
            screen.blit(grass2,(600,225))
            screen.blit(grass2,(750,310))
            screen.blit(grass,(525,250))
            screen.blit(grass,(720,300))
            screen.blit(grass,(720,275))
        # once the altar has been used the boss fight begins
        if altar.used == True:
            # drawing the boss
            dragon_sprites.draw(screen)
            # attacks only occur if the boss is not exhausted
            if vulcan.exhausted == False:
                attacks.current_dragon = "vulcan"
                # updating boss attacks
                attacks.attackupdate()
                damage_sprites.update()
                damage_sprites.draw(screen)

        # drawing and updating all sprite groups    
        moving_sprites.draw(screen)
        moving_sprites.update()
        player_sprite.draw(screen)
        # updating player animations
        player_sprite.update()
        player.updateattack()
        player.updatewalk()
        player.update()
        player.updateidle()
        # updating player movement
        player.movement()
        # updating explosion animation
        explosion.updateexplosion()
        # updating player health
        healthbar.update()
        # updating boss exhaustion state
        vulcan.exhaustion()

        # if the player dies the death screen is triggered
        if healthbar.death == True:
            running = False
            # resetting game state so it can restart cleanly
            vulcan.health = 15
            vulcan.exhausted = False
            vulcan.exhaustion_start = 0
            vulcan.lastexhaustion = pygame.time.get_ticks()
            player.rect.x = 575
            player.rect.y = 600
            moving_sprites.add(altar)
            player_sprite.empty()
            player_sprite.add(player)
            vulcan = Vulcan(375,25)
            dragon_sprites.empty()
            dragon_sprites.add(vulcan)
            moving_sprites.remove(explosion)
            moving_sprites.add(explosion)
            screen.blit(background, (0, 0))
            damage_sprites.empty()
            attacks = Attacks()
            damage_sprites.add(attacks)
            attacks.current_dragon = 0
            altar.used = False
            healthbar.death = False
            healthbar.currenthealthsprite = 0
            death_screen()
        # if the boss dies the victory screen is triggered
        if vulcan.death == True:
            running = False
            # resetting the game in the same way as the death reset
            vulcan.health = 15
            vulcan.exhausted = False
            vulcan.exhaustion_start = 0
            vulcan.lastexhaustion = pygame.time.get_ticks()
            player.rect.x = 575
            player.rect.y = 600
            moving_sprites.add(altar)
            player_sprite.empty()
            player_sprite.add(player)
            vulcan = Vulcan(375,25)
            dragon_sprites.empty()
            dragon_sprites.add(vulcan)
            moving_sprites.remove(explosion)
            moving_sprites.add(explosion)
            screen.blit(background, (0, 0))
            damage_sprites.empty()
            attacks = Attacks()
            damage_sprites.add(attacks)
            attacks.current_dragon = 0
            altar.used = False
            healthbar.death = False
            healthbar.currenthealthsprite = 0
            victory_screen()
            

        if altar.used == True:
            misc_sprites.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    vulcan.health = 15
                    vulcan.exhausted = False
                    vulcan.exhaustion_start = 0
                    vulcan.lastexhaustion = pygame.time.get_ticks()
                    player.rect.x = 575
                    player.rect.y = 600
                    moving_sprites.add(altar)
                    player_sprite.empty()
                    player_sprite.add(player)
                    vulcan = Vulcan(375,25)
                    dragon_sprites.empty()
                    dragon_sprites.add(vulcan)
                    moving_sprites.remove(explosion)
                    moving_sprites.add(explosion)
                    screen.blit(background, (0, 0))
                    damage_sprites.empty()
                    attacks = Attacks()
                    damage_sprites.add(attacks)
                    attacks.current_dragon = 0
                    altar.used = False
                    healthbar.death = False
                    healthbar.currenthealthsprite = 0

                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.animateattack()
                    attack_zone = interaction_rect(vulcan, 30)
                    if vulcan.exhausted == True and player.rect.colliderect(attack_zone):
                        if vulcan.current_time-vulcan.last_hit>=vulcan.iframe:
                            vulcan.health-=1
                            print("hit")
                            vulcan.last_hit=vulcan.current_time
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    altar_zone = interaction_rect(altar, 60)
                    if player.rect.colliderect(altar_zone):
                        if altar.used == False:
                            explosion.activateexplosion()
                            explosion.updateexplosion()
                            altar.interact()
                            show_grass = False
            
            
        
        keys = pygame.key.get_pressed()
        altar_zone = interaction_rect(altar, 60)
        if player.rect.colliderect(altar_zone) and altar.used == False:
            draw_text("Press E to interact", button_font, (255,255,25) ,
            altar.rect.x - 10, altar.rect.y - 30)


        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.upkey()
            player.animatewalk()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.rightkey()
            player.animatewalk()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.leftkey()
            player.animatewalk()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.downkey()
            player.animatewalk()
        

        pygame.display.update()
        mainClock.tick(60)

def postgame():
    running = True
    while running:
        pygame.display.set_caption("Post Game")
        screen.fill((58,55,58))
        draw_text("Post-Game",title_font, (37, 35, 33),475,175)

        impossible_button = pygame.Rect((445,300, 150, 100))
        nohit_button = pygame.Rect((750, 300, 150, 100))

        pygame.draw.rect(screen, (253, 101, 45), impossible_button)
        pygame.draw.rect(screen, (253, 101, 45), nohit_button)

        text_surface3 = button_font.render("Impossible", True, (37, 35, 33 ))
        text_rect3 = text_surface3.get_rect(center=impossible_button.center)
        screen.blit(text_surface3, text_rect3)

        text_surface4 = button_font.render("No-Hit", True, (37, 35, 33 ))
        text_rect4 = text_surface4.get_rect(center=nohit_button.center)
        screen.blit(text_surface4, text_rect4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
      
        pygame.display.update()
        mainClock.tick(60)

main_menu()
            


