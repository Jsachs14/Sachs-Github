import pygame 
import math
import time
import sys
from PIL import Image
import random



#getting game sprites from resources.png

#player

player_init = Image.open("resources.png").crop((77,5,163,96)).convert("RGBA")
player_init = player_init.resize(list(map(lambda x:x//2 , player_init.size)))


player_frame_1 = Image.open("resources.png").crop((1679,2,1765,95)).convert("RGBA")
player_frame_1 = player_frame_1.resize(list(map(lambda x:x//2 , player_frame_1.size)))

player_frame_2 = Image.open("resources.png").crop((1767,2,1853,95)).convert("RGBA")
player_frame_2 = player_frame_2.resize(list(map(lambda x:x//2 , player_frame_2.size)))

player_frame_3 = Image.open("resources.png").crop((1855,2,1941,95)).convert("RGBA")
player_frame_3 = player_frame_3.resize(list(map(lambda x:x//2 , player_frame_3.size)))

player_frame_31 = Image.open("resources.png").crop((1943,2,2029,95)).convert("RGBA")
player_frame_31 = player_frame_31.resize(list(map(lambda x:x//2 , player_frame_31.size)))

player_frame_4 = Image.open("resources.png").crop((2030,2,2117,95)).convert("RGBA")
player_frame_4 = player_frame_4.resize(list(map(lambda x:x//2 , player_frame_4.size)))

player_frame_5 = Image.open("resources.png").crop((2207,2,2323,95)).convert("RGBA")
player_frame_5 = player_frame_5.resize(list(map(lambda x:x//2 , player_frame_5.size)))

player_frame_6 = Image.open("resources.png").crop((2324,2,2441,95)).convert("RGBA")
player_frame_6 = player_frame_6.resize(list(map(lambda x:x//2 , player_frame_6.size)))

cloud = Image.open("resources.png").crop((166,2,257,29)).convert("RGBA")
cloud = cloud.resize(list(map(lambda x:x//2 , cloud.size)))

ground = Image.open("resources.png").crop((2,102,2401,127)).convert("RGBA")
ground = ground.resize(list(map(lambda x:x//2 , ground.size)))

obstacle1 = Image.open("resources.png").crop((446,2,479,71)).convert("RGBA")
obstacle1 = obstacle1.resize(list(map(lambda x:x//2 , obstacle1.size)))

obstacle2 = Image.open("resources.png").crop((446,2,547,71)).convert("RGBA")
obstacle2 = obstacle2.resize(list(map(lambda x:x//2 , obstacle2.size)))

obstacle3 = Image.open("resources.png").crop((446,2,581,71)).convert("RGBA")
obstacle3 = obstacle3.resize(list(map(lambda x:x//2 , obstacle3.size)))

obstacle4 = Image.open("resources.png").crop((653,2,701,101)).convert("RGBA")
obstacle4 = obstacle4.resize(list(map(lambda x:x//2 , obstacle4.size)))

obstacle5 = Image.open("resources.png").crop((653,2,701,101)).convert("RGBA")
obstacle5 = obstacle5.resize(list(map(lambda x:x//2 , obstacle5.size)))

obstacle5 = Image.open("resources.png").crop((653,2,749,101)).convert("RGBA")
obstacle5 = obstacle5.resize(list(map(lambda x:x//2 , obstacle5.size)))

obstacle6 = Image.open("resources.png").crop((851,2,950,101)).convert("RGBA")
obstacle6 = obstacle6.resize(list(map(lambda x:x//2 , obstacle6.size)))

pygame.init()
speed = 1

leg_time = 1
leg_interval = 50

# creating window
screen = pygame.display.set_mode((600, 200))
pygame.display.set_caption("Pygame Dino Game")

c_x=600
c_y=10

jump_height = 0
jump_margin = 1
jump_phase = 0

rand_ob_start = random.randint(1, 6)
rand_obs = 0

if (rand_ob_start == 1):
    sprite = obstacle1
elif (rand_ob_start == 2):
    sprite = obstacle2
elif (rand_ob_start == 3):
    sprite = obstacle3
elif (rand_ob_start == 4):
    sprite = obstacle4
elif (rand_ob_start == 5):
    sprite = obstacle5
elif (rand_ob_start == 6):
    sprite = obstacle6

obs_x = 600
obs_rate = 1

jump = False
moving_up = True
game_over = False

# Define ground color
white = (255, 255, 255)
black = (0, 0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_SPACE):
                jump = True

        

    

    # Fill the screen with white color
    screen.fill(white)

    # Draw ground
    screen.blit(pygame.image.fromstring(ground.tobytes(), ground.size, ground.mode), (0, 150))

    # screen.blit(pygame.image.fromstring(player_init.tobytes(), player_init.size, player_init.mode), (20, 135))

    if jump == False:
        if (leg_time < leg_interval+1):
            #player_frame_3
            screen.blit(pygame.image.fromstring(player_frame_3.tobytes(), player_frame_3.size, player_frame_3.mode), (60, 135))
        else:
            #player_frame_31
            screen.blit(pygame.image.fromstring(player_frame_31.tobytes(), player_frame_31.size, player_frame_31.mode), (60, 135))

            if (leg_time == (leg_interval*2)):
                leg_time = 0

        leg_time = leg_time + 1

        if (obs_x < 60):
            game_over = True






    else:
        #4 phases of jump --> moving up fast, slow, moving down slow and fast
        #moving up fast --> 0
        #moving up slow --> 1
        #moving down slow --> 2 (skipped for now)
        #moving down fast --> 3
        if (jump_phase == 0):
            jump_height += 1.5
            if (jump_height >= 90):
                jump_phase = 1
        
        elif (jump_phase == 1):
            jump_height += .5
            if (jump_height >= 95):
                jump_phase = 3

        elif (jump_phase == 2):
            jump_height -= .5
            if (jump_height <= 90):
                jump_phase = 3
        
        elif (jump_phase == 3):
            jump_height -= 1.5
            if (jump_height <= 0):
                jump = False
                jump_phase = 0

        
        screen.blit(pygame.image.fromstring(player_frame_1.tobytes(), player_frame_1.size, player_frame_1.mode), (60, 135 - jump_height))

    





        
    if(c_x == 600):
        rand = random.randint(1, 4)

        if (rand == 1):
            c_y = 10
        elif (rand == 2):
            c_y = 20
        elif (rand == 3):
            c_y = 30
        elif (rand == 4):
            c_y = 40

    screen.blit(pygame.image.fromstring(cloud.tobytes(), cloud.size, cloud.mode), (c_x, c_y))

    c_x = c_x - .25

    if (c_x == 0):
        c_x = 600




    screen.blit(pygame.image.fromstring(sprite.tobytes(), sprite.size, sprite.mode), (obs_x, 135))

    obs_x = obs_x - obs_rate

    if (obs_x == 0):
        obs_x = 600
        rand_obs = random.randint(1, 6)

        #spaces to see hits in terminal
        # print("")
        # print("")
        # print("")

        if (rand_obs == 1):
            sprite = obstacle1
        elif (rand_obs == 2):
            sprite = obstacle2
        elif (rand_obs == 3):
            prite = obstacle3
        elif (rand_obs == 4):
            sprite = obstacle4
        elif (rand_obs == 5):
            sprite = obstacle5



    if (game_over == True):
        screen.fill(white)
        game_over_text = pygame.font.Font('freesansbold.ttf', 32)
        text = game_over_text.render('GAME OVER', True, black, white)
        textRect = text.get_rect()
        textRect.center = (300, 100)
        screen.blit(text, textRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_SPACE):
                    #resetting game
                    game_over = False
                    obs_x = 600
                    jump = False
                    jump_height = 0
                    jump_phase = 0

                    #figure out resetting


            

        

    

    
        


    pygame.display.flip()

        

    



    
