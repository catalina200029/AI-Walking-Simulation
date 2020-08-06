import pygame
#import neat
import time
from PIL import Image
import os
import math
import random

pygame.init()

WIN_WIDTH = 900
WIN_HEIGHT = 600
BORDER = 3

FACE = pygame.transform.scale(pygame.image.load('face2.png'), (100, 100))

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

run = True


class Floor:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def display(self):
        pygame.draw.rect(win, (0, 0, 0), (self.x - 1, self.y - 1, self.w + 2, self.h + 2))
        pygame.draw.rect(win, (255, 255, 0), (self.x, self.y, self.w, self.h))


class Leg:
    HEIGHT = 70

    def __init__(self, x, y):
        self.angle = 90
        self.angleD = 90
        self.x = x
        self.y = y
        self.x2 = self.x
        self.y2 = self.y + self.HEIGHT
        self.xD = self.x
        self.yD = self.y + self.HEIGHT
        self.xD2 = self.x2
        self.yD2 = self.y2 + self.HEIGHT

    def display(self):
        pygame.draw.line(win, (0, 0, 0), (self.x, self.y), (self.x2, self.y2), BORDER)
        pygame.draw.line(win, (0, 0, 0), (self.xD, self.yD), (self.xD2, self.yD2), BORDER)

    def updateLeg(self, rotation):
        c = math.cos(rotation * math.pi / 180)
        s = math.sin(rotation * math.pi / 180)

        self.x2 -= self.x
        self.y2 -= self.y

        xnew = self.x2 * c - self.y2 * s
        ynew = self.x2 * s + self.y2 * c

        self.x2 = xnew + self.x
        self.y2 = ynew + self.y

    def updateLegD(self, rotation):
        c = math.cos(rotation * math.pi / 180)
        s = math.sin(rotation * math.pi / 180)

        self.xD2 -= self.xD
        self.yD2 -= self.yD

        xnew = self.xD2 * c - self.yD2 * s
        ynew = self.xD2 * s + self.yD2 * c

        self.xD2 = xnew + self.xD
        self.yD2 = ynew + self.yD

    def rotate(self, rotation):
        xDif = self.x2
        yDif = self.y2

        self.angle += rotation
        self.angleD += rotation
        self.updateLeg(rotation)
        self.updateLegD(rotation)

        xDif -= self.x2
        yDif -= self.y2

        self.xD -= xDif
        self.yD -= yDif
        self.xD2 -= xDif
        self.yD2 -= yDif

    def rotateD(self, rotation):
        self.angleD += rotation
        self.updateLegD(rotation)

    def move(self):
        self.x += 5
        self.x2 +=5
        self.xD += 5
        self.xD2 +=5

    def isFalling(self):
        touches = -1000

        if math.floor(self.x2 - 200) <= 0.1:
            touches = self.x2

        if math.floor(self.x2 - 200) <= 0.1:
            touches = self.x2

        return touches


class Creature:
    HEIGHT = 100
    WIDTH = 100

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rotation = 0
        self.leg1 = Leg(self.x, self.y + self.HEIGHT)
        self.leg2 = Leg(self.x + self.WIDTH, self.y + self.HEIGHT)

    def move(self):
        self.x += 5

    def display(self):
        win.blit(FACE, (self.x, self.y))
        self.leg1.display()
        self.leg2.display()

    def checkGround(self):
        #if self.leg1.isFalling() != -1000:
        pass


player = Creature(200, 500 - 140 - 100)
floor = Floor(0, 500, WIN_WIDTH, 200)

while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False

    if not run:
        break

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        player.move()
        player.leg1.move()
        player.leg2.move()

    if keys[pygame.K_q]:
        player.leg1.rotate(5)
    if keys[pygame.K_w]:
        player.leg1.rotate(-5)

    if keys[pygame.K_e]:
        player.leg2.rotate(5)
    if keys[pygame.K_r]:
        player.leg2.rotate(-5)

    if keys[pygame.K_a]:
        player.leg1.rotateD(5)
    if keys[pygame.K_s]:
        player.leg1.rotateD(-5)

    if keys[pygame.K_d]:
        player.leg2.rotateD(5)
    if keys[pygame.K_f]:
        player.leg2.rotateD(-5)

    pygame.draw.rect(win, (220, 220, 220), (0, 0, WIN_WIDTH, WIN_HEIGHT))

    player.display()
    floor.display()

    pygame.display.update()

pygame.quit()