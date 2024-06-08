import pygame
import random
from time import sleep

pygame.init()
screen = pygame.display.set_mode((520, 520))
clock = pygame.time.Clock()
running = True
self = [480, 480]
last_move = [0, 0]
current_move = [0, 0]
framecounter = 0
tail = []
length = 1
apple = None
alive = True

def game_over():
    global alive, framecounter
    framecounter = 1
    alive = False
    
    pygame.event.post(pygame.event.Event(pygame.QUIT))

def add_apple():
    global apple, tail
    while True:
        apple = [random.randint(0, 12) * 40, random.randint(0, 12) * 40]
        for i in tail:
            if apple[0] == i[0] and apple[1] == i[1]:
                break
        else:
            break

def add_tail():
    tail.append([self[0], self[1], length])

def draw_tail():
    global length
    global apple
    for i in tail:
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), pygame.Rect(i[0], i[1], 40, 40))
        i[2] -= 1
        if i[2] == 0:
            tail.remove(i)

def movement(keys):
    # register possible moves on every frame
    # every fifteenth frame move the snake and add a tail
    global last_move, current_move, apple, length
    if keys[pygame.K_UP] and last_move != [0, 40]:
        current_move = [0, -40]
    elif keys[pygame.K_DOWN] and last_move != [0, -40]:
        current_move = [0, 40]
    elif keys[pygame.K_LEFT] and last_move != [40, 0]:
        current_move = [-40, 0]
    elif keys[pygame.K_RIGHT] and last_move != [-40, 0]:
        current_move = [40, 0]
    
    if framecounter % 15 == 0 and current_move != [0, 0]:
        self[0] += current_move[0]
        self[1] += current_move[1]
        last_move = current_move
        for i in tail:
            if self[0] == i[0] and self[1] == i[1]:
                game_over()
    
    if self[0] < 0 or self[0] > 480 or self[1] < 0 or self[1] > 480:
        game_over()
    
    if self[0] == apple[0] and self[1] == apple[1]:
        add_apple()
        length += 15

    add_tail()

add_apple()

while running:
    framecounter+=1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("black")

    if alive:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        movement(keys)

        pygame.draw.rect(screen, pygame.Color(255, 0, 0), pygame.Rect(apple[0], apple[1], 40, 40))

        draw_tail()

        pygame.display.flip()
    else:
        fontObj = pygame.font.SysFont("menlo",  64)
        textSufaceObj = fontObj.render('GAME OVER', True, (255, 255, 255), None)
        screen.blit(textSufaceObj, (250 - 32 * 5, 250-32))
        pygame.display.flip()
        sleep(5)
        running = False
    clock.tick(60)

pygame.quit()