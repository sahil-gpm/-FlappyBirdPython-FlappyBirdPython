import pygame
from pygame import mixer
from pygame.locals import *
import random
import time

fps = 50
pygame.init()
mixer.init()
clock = pygame.time.Clock()
SCREENWIDTH = 800
SCREENHEIGHT = 600
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Flappy Bird Tutorial")

font = pygame.font.SysFont(None,35)
fontGAMEOVER = pygame.font.SysFont(None,55)

def blitAftergameOver(text,color,x,y):
    render_font = fontGAMEOVER.render(text,True,color)
    SCREEN.blit(render_font,[x,y])

def blitText(text,color,x,y):
    render_font = font.render(text,True,color)
    SCREEN.blit(render_font,[x,y])

# loading images or sprites
bgImage = pygame.image.load('flappy/flapImg/gallery/sprites/bg.png').convert()
pygame.transform.scale(bgImage,(SCREENWIDTH,SCREENHEIGHT)).convert_alpha()
base = pygame.image.load('flappy/flapImg/gallery/sprites/ground.png').convert()
player = pygame.image.load('flappy/flapImg/gallery/sprites/bird.png')
pipe = pygame.image.load('flappy/flapImg/gallery/sprites/pipe.png')
pipe_rotate = pygame.transform.rotate(pipe,180)

# loading audio --> 
wing = ('flappy/flapImg/gallery/audio/wing.wav')
point = ('flappy/flapImg/gallery/audio/point.wav')
red = (255,0,0)
white = (255,255,255)

def gameOver(fps):
    pygame.mixer.music.load('flappy/flapImg/gallery/audio/death.mp3')
    pygame.mixer.music.play()
    gover = pygame.image.load('flappy/flapImg/gallery/sprites/gameOver.jpg')
    gover = pygame.transform.scale(gover,(SCREENWIDTH,SCREENHEIGHT))
    while True:
        SCREEN.blit(gover,(0,0))
        blitAftergameOver("PRESS ENTER TO PLAY AGAIN",(255,255,255),135,300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startGame(fps)
        clock.tick(fps)
        pygame.display.update()

def startGame(fps):
    baseb = 0
    baseb_move = -4
    start = pygame.image.load('flappy/flapImg/gallery/sprites/bg.png')
    txt = pygame.image.load('flappy/flapImg/gallery/sprites/text.png')
    start = pygame.transform.scale(start,(SCREENWIDTH,SCREENHEIGHT))
    loop = ('flappy/flapImg/gallery/audio/loop.mp3') 
    pygame.mixer.music.load(loop)
    pygame.mixer.music.play() # playing the music

    while True:
        SCREEN.blit(start,(0,0))
        SCREEN.blit(txt,(215,120))
        SCREEN.blit(base,(baseb,SCREENHEIGHT - base.get_height()))
        SCREEN.blit(player,(400,360))
        blitText("PRESS ESCAPE OR SPACE TO PLAY",(255,255,255),200,300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    mainGame() 
        baseb += baseb_move
        if abs(baseb) > 35:
            baseb = 0

        clock.tick(fps)
        pygame.display.update()

def mainGame():

    # GAME VARIABLES DECLARED INSIDE THE FUNCTION ----> 
    base_x = 0 # blitting position of base
    base_x_move = -4 # moving speen of base to left
    player_x = 50 # initial position of bird in  x-axis
    player_y = (SCREENHEIGHT / 2) - 50 # initial position of bird in  y-axis
    player = pygame.image.load('flappy/flapImg/gallery/sprites/bird.png') # loading the bird image
    player_y_decrement = 1  # setting gravity of bird
    pipeX = 400 # initial x-position of pipe
    pipeY = random.randint(270,350) + 40 # selecting pipe_y position of lower pipe by using random
    pipeYupper = random.randint(320,410)  # selecting pipe_y position of upper pipe by using random
    pipeYupper = -(pipeYupper) # upper pipe-Y position
    score = 0 # initializing score to zero
    fps = 50 # frame - rate

    time.sleep(1.5) 
    isRunning = True
    while isRunning:
        player_y += player_y_decrement
        # creating a moving bg by decrementing base_x by 4
        if abs(base_x) > 20:
            base_x = 0

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                isRunning = False
                pygame.quit()

            if (event.type == pygame.MOUSEBUTTONDOWN):
                player_y_decrement = 4
        
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                player_y_decrement = -5
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()

            if (event.type == pygame.KEYUP and event.key == pygame.K_UP):
                player_y_decrement = 3
            
        SCREEN.blit(bgImage,(0,0))
        SCREEN.blit(pipe,(pipeX,pipeY))
        SCREEN.blit(pipe_rotate,(pipeX,pipeYupper))
        SCREEN.blit(base,(base_x,SCREENHEIGHT - base.get_height() + 50))
        SCREEN.blit(player,(player_x,player_y))
        base_x += base_x_move
        pipeX += base_x_move
        pipeX += base_x_move

        # pipe stepping towards left ---> 
        if(pipeX <= -80):
            pipeX = SCREENWIDTH + 10
            pipeY = random.randint(280,440)
            pipeYupper = random.randint(300,350) + 50
            pipeYupper = -(pipeYupper)
            
        # checking for score
        playerMid = player_x + (player.get_width()/2)
        pipeMid = pipeX + (pipe.get_width()/2)
        if pipeMid < playerMid < pipeMid + 10:
            pygame.mixer.music.load(point)
            pygame.mixer.music.play()
            score += 10
            fps += 1

        # handling collisions ---> 
        pipeHeight = pipe.get_height()
        pipeWidth = pipe.get_width()

        # crashing logic
        if player_y >= (SCREENHEIGHT - base.get_height() + 50):
            player_y_decrement = 0
            player = pygame.transform.rotate(player,-180)
            isRunning = False

        # for upper pipe ---> 
        if player_y  < pipeHeight + pipeYupper  and abs(player_x - 55 - pipeX) < pipeWidth:
            isRunning = False

        # for lower pipe --->
        if player_y  + player.get_height() > pipeY and abs(player_x - 55 - pipeX) < pipeWidth:
            isRunning = False

        # player touches the ceiling ---> 
        if player_x <= 0:
            isRunning = False
            
        if (isRunning == False):
            gameOver(fps)

        # maintaining the fps
        blitText("Current score : "+str(score),red,8,20)
        clock.tick(fps)
        pygame.display.update()

if __name__ == '__main__':
    # startGame()
    startGame(fps)
# Finally --> I created it on my own !!!!!