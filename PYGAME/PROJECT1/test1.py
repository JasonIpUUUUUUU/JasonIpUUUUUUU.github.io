import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PIXEL_SIZE = 20

speed = 10
jumpForce = 200
dashCooldown = 20
gravity = 1

screen_width = 864
screen_height = 936

floor_rect = pygame.Rect(0, HEIGHT/1.5, WIDTH, HEIGHT)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PIXEL JOUSTING")

p1_x = WIDTH // 2 * 1.5
p1_y = HEIGHT // 2

p2_x = WIDTH // 2 / 1.5
p2_y = HEIGHT // 2

running = True

p1Alive = True
p2Alive = True

p1Invincible = False
p2Invincible = False

p1Max = False
p2Max = False

p1_grav = 0
p2_grav = 0

p1_jumpVel = jumpForce/4
p2_jumpVel = jumpForce/4

p1_timer = 0
p2_timer = 0

p1_prevTime = 0
p2_prevTime = 0

p1_prevKey = ""
p2_prevKey = ""

p1_rect = pygame.Rect(p1_x, p1_y, PIXEL_SIZE, PIXEL_SIZE)
p2_rect = pygame.Rect(p2_x, p2_y, PIXEL_SIZE, PIXEL_SIZE)

def isFalling(xPos, yPos):
    if pixel_rect := pygame.Rect(xPos, yPos, PIXEL_SIZE, PIXEL_SIZE):
        if pixel_rect.colliderect(floor_rect):
            return False
        else:
            return True
        
def attack(startX, endX, yPos, attackingPlayer):
    attackWidth = startX - endX
    if(attackWidth < 0):
        attackWidth *= -1
    attack_rect = pygame.Rect((startX + endX)/2, yPos, attackWidth, PIXEL_SIZE)
    check_collision(attack_rect, attackingPlayer)

def check_collision(player1_rect, player2_rect):
    global p1Alive, p2Alive
    if(player1_rect.colliderect(player2_rect)):
        if(p1Invincible and not p2Invincible):
            p2Alive = False
        elif(p2Invincible and not p1Invincible):
            p1Alive = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                p1_prevKey = "a"
                p1_prevTime = 5
            elif event.key == pygame.K_d:
                p1_prevKey = "d"
                p1_prevTime = 5
            elif event.key == pygame.K_LEFT :
                p2_prevKey = "left"
                p2_prevTime = 5
            elif event.key == pygame.K_RIGHT:
                p2_prevKey = "right"
                p2_prevTime = 5

    keys = pygame.key.get_pressed()
    if(keys[pygame.K_a]):
        if(p1_prevTime > 0 and p1_prevKey == "a" and p1_timer == 0):
            p1Invincible = True
            p1startX = p1_x
            for x in range(100):
                p1_x -= 1
            p1endX = p1_x
            attack(p1startX, p1endX, p1_y, p2_rect)
            p1_prevKey = ""
            p1_timer = dashCooldown
            p1Invincible = False
        else:
            p1_x -= speed
    if(keys[pygame.K_d]):
        if(p1_prevTime > 0 and p1_prevKey == "d" and p1_timer == 0):
            p1Invincible = True
            p1startX = p1_x
            for x in range(100):
                p1_x += 1
            p1endX = p1_x
            attack(p1startX, p1endX, p1_y, p2_rect)
            p1_prevKey = ""
            p1_timer = dashCooldown
            p1Invincible = False
        else:
            p1_x += speed
    if keys[pygame.K_LEFT]:
        if(p2_prevTime > 0 and p2_prevKey == "left" and p2_timer == 0):
            p2Invincible = True
            p2startX = p2_x
            for x in range(100):
                p2_x -= 1
            p2endX = p2_x
            attack(p2startX, p2endX, p2_y, p1_rect)
            p2_prevKey = ""
            p2_timer = dashCooldown
            p2Invincible = False
        else:
            p2_x -= speed
    if keys[pygame.K_RIGHT]:
        if(p2_prevTime > 0 and p2_prevKey == "right" and p2_timer == 0):
            p2Invincible = True
            p2startX = p2_x
            for x in range(100):
                p2_x += 1
            p2endX = p2_x
            attack(p2startX, p2endX, p2_y, p1_rect)
            p2_prevKey = ""
            p2_timer = dashCooldown
            p2Invincible = False
        else:
            p2_x += speed


    screen.fill((0, 0, 0))

    if(isFalling(p1_x, p1_y)):
        p1_y += p1_grav
        p1_grav += gravity
    else:
        p1_grav = gravity
        if(keys[pygame.K_w]):
            if(p1Max and p1_jumpVel < jumpForce):
                p1_jumpVel += 1
            else:
                p1Max = True
                p1_jumpVel -= 1
            p1_y -= p1_jumpVel
        else:
            p1_y = floor_rect.top - 15
            p1_jumpVel = jumpForce/4
            p1Max = False
    p1_rect.topleft = (p1_x, p1_y)

    if(isFalling(p2_x, p2_y)):
        p2_y += p2_grav
        p2_grav += gravity
    else:
        p2_grav = gravity
        if(keys[pygame.K_UP]):
            if(p2Max and p2_jumpVel < jumpForce):
                p2_jumpVel += 1
            else:
                p2Max = True
                p2_jumpVel -= 1
            p2_y -= p2_jumpVel
        else:
            p2_y = floor_rect.top - 15
            p2_jumpVel = jumpForce/4
            p2Max = False
    p2_rect.topleft = (p2_x, p2_y)

    pygame.draw.rect(screen, WHITE, floor_rect)
    if(p1Alive):
        pygame.draw.rect(screen, RED, (p1_x, p1_y, PIXEL_SIZE, PIXEL_SIZE))

    if(p2Alive):
        pygame.draw.rect(screen, BLUE, (p2_x, p2_y, PIXEL_SIZE, PIXEL_SIZE))
    if p1_timer > 0:
        p1_timer -= 1
    if p2_timer > 0:
        p2_timer -= 1

    p1_prevTime -= 1
    p2_prevTime -= 1

    pygame.display.flip()
    clock.tick(20)

pygame.quit()