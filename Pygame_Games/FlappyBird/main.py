import random
import sys
import pygame
from pygame.locals import *


#GLOBAL VARIABLES
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

#Other Variables
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'FlappyBird/resources/SPRITES//bird.png'
BACKGROUND = 'FlappyBird/resources/SPRITES//bg.jpeg'      
PIPE = 'FlappyBird/resources/SPRITES//pipe.png'




def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2
    messagex = int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0

    playbutton= pygame.Rect(108,222,68,65)
    


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if pygame.mouse.get_pos()[0] > playbutton[0] and pygame.mouse.get_pos()[0] < playbutton[0] + playbutton[2]:
                if pygame.mouse.get_pos()[1] > playbutton[1] and pygame.mouse.get_pos()[1] < playbutton[1] + playbutton[3]:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if playbutton.collidepoint(pygame.mouse.get_pos()):
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mainGame()
            

            else:
                SCREEN.blit(GAME_SPRITES['background'], (0,0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']}]
    
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']}]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 #velocity while flapping
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return

        
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if(playerVelY<playerMaxVelY and not playerFlapped):
            playerVelY += playerAccY
        
        if playerFlapped:
            playerFlapped = False
        playerHeight= GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        #move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        #add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])
        
        #if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/4.5
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper pipe
        {'x': pipeX, 'y': y2} #lower pipe
    ]
    return pipe

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        gameOver()
    #UPPER PIPES
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            print(playerx,pipe['x'],)
            gameOver()

    #LOWER PIPES
    for pipe in lowerPipes:
        if(playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            gameOver()

    return False

def gameOver():
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird by Jonah')
    GAME_SPRITES['OVER']=pygame.image.load('FlappyBird/resources/SPRITES/gameover.png').convert_alpha()
    GAME_SPRITES['RETRY']=pygame.image.load('FlappyBird/resources/SPRITES/retry.png').convert_alpha()
    GAME_SPRITES['HOME']=pygame.image.load('FlappyBird/resources/SPRITES/home.png').convert_alpha()

    SCREEN.blit(GAME_SPRITES['background'], (0,0))
    SCREEN.blit(GAME_SPRITES['base'], (0, GROUNDY))
    SCREEN.blit(GAME_SPRITES['OVER'],(0,0))
    SCREEN.blit(GAME_SPRITES['RETRY'],(30,220))
    SCREEN.blit(GAME_SPRITES['HOME'],(30,280))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN and (event.key == K_SPACE):
                mainGame()

            #RETRY BUTTON
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if pygame.mouse.get_pos()[0]>30 and pygame.mouse.get_pos()[0]<30+GAME_SPRITES['RETRY'].get_width():
                if pygame.mouse.get_pos()[1]>220 and pygame.mouse.get_pos()[1]<220+GAME_SPRITES['RETRY'].get_height():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mainGame()
            
            #HOME BUTTON
            if pygame.mouse.get_pos()[0]>30 and pygame.mouse.get_pos()[0]<30+GAME_SPRITES['HOME'].get_width():
                if pygame.mouse.get_pos()[1]>280 and pygame.mouse.get_pos()[1]<280+GAME_SPRITES['HOME'].get_height():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        welcomeScreen()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    

#START GAME
if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by @Jonah')


    #Loading Sprites
    GAME_SPRITES['numbers'] = (
        pygame.image.load('FlappyBird/resources/SPRITES//0.png').convert_alpha(),
        pygame.image.load('FlappyBird/resources/SPRITES//1.png').convert_alpha(),
        pygame.image.load('FlappyBird/resources/SPRITES//2.png').convert_alpha(),
        pygame.image.load('FlappyBird/resources/SPRITES//3.png').convert_alpha(),
        pygame.image.load('FlappyBird/resources/SPRITES//4.png').convert_alpha(),
        pygame.image.load('FlappyBird/resources/SPRITES//5.png').convert_alpha(),
        pygame.image.load('FlappyBird/resources/SPRITES//6.png').convert_alpha(),
        pygame.image.load('FlappyBird/resources/SPRITES//7.png').convert_alpha(),
        pygame.image.load('FlappyBird/resources/SPRITES//8.png').convert_alpha(),
        pygame.image.load('FlappyBird/resources/SPRITES//9.png').convert_alpha(),
    )

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['message']= pygame.image.load('FlappyBird/resources/SPRITES//message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('FlappyBird/resources/SPRITES//base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),pygame.image.load(PIPE).convert_alpha())


    #Loading Sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('FlappyBird/resources/AUDIO//die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('FlappyBird/resources/AUDIO//hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('FlappyBird/resources/AUDIO//point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('FlappyBird/resources/AUDIO//swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('FlappyBird/resources/AUDIO//wing.wav')

    while True:
        welcomeScreen()
        mainGame()

    
    
