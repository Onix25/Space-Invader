import pygame
import math
import random

from pygame import mixer


# initialize the pygame
pygame.init()

# create the screen
# width and height respectively
screen = pygame.display.set_mode((800, 600))

# Tile and ICOn
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
#background music
mixer.music.load('background.wav')
mixer.music.play(-1)
# player
playerimg = pygame.image.load('spaceship.png')
playerx = 370
playery = 480
num = 0
# enemyu
enemyimg = []
enemyx = []
enemyy = []
num1 = []
num2 = []
num_enemies = 6
for i in range(num_enemies):
    enemyimg.append(pygame.image.load('alien.png'))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50, 150))
    num1.append(0.3)
    num2.append(40)

# BULLET
bulletimg = pygame.image.load('bullet.png')
bullet_state = "ready"
bulletx = 0
bullety = 480
num1_b = 0
num2_b = 2


# now we dont want this player to disappear then we want to call this function iside while loop
def player(x, y):
    screen.blit(playerimg, (x, y))  # blit means to draw on the screen


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))  # blit means to draw on the screen


def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 3, y + 10))  # blit means to draw on the screen


# collision
def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow(enemyx - bulletx, 2) + math.pow(enemyy - bullety, 2))
    if distance <= 27:
        return True
    else:
        return False


score_value = 0
font = pygame.font.Font('Good Things.ttf', 32)
textx = 10
texty = 10
game_over_font = pygame.font.Font('Good Things.ttf', 64)
def print_game_over() :
    over_text =  game_over_font.render("Game Over : " , True, (255, 255, 255))
    screen.blit(over_text, (250, 250))

def print_score(x, y):
    score =font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# game loop
running = True
while running:
    screen.fill((150, 0, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # keystrokes mechanics
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                num = -0.4
            if event.key == pygame.K_RIGHT:
                num = 0.4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletx = playerx
                    bullet_fire(bulletx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                num = 0

    playerx += num

    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

        #enemy movement
    for i in range(num_enemies):

        if enemyy[i] >440 :
            for j  in range(num_enemies):
             enemyy[j] = 2000
            print_game_over()
            break


        enemyx[i] += num1[i]
        if enemyx[i] <= 0:
            num1[i] = 0.3
            enemyy[i] += num2[i]
        elif enemyx[i] >= 736:
            num1[i] = -0.3
            enemyy[i] += num2[i]
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        # collisions
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bullety = 480
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(50, 150)

        enemy(enemyx[i], enemyy[i], i)

    # Bullet Movement
    if bullet_state == "fire":
        bullet_fire(bulletx, bullety)
        bullety -= num2_b
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"

    player(playerx, playery)
    print_score(textx, texty)
    pygame.display.update()
