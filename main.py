# base file
import os
import sys
import math
import random
import pygame

WIDTH = 623
HEIGHT = 150

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('DINO GAME')


class BackGround:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.set_texture()
        self.show()

    def show(self):
        screen.blit(self.texture, (0, 0))

    def set_texture(self):
        path = os.path.join('assets/images/bg.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))



class Game:

    def __init__(self):
        self.bg = BackGround()

def main():

    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()



main()

