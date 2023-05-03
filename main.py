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
    '''
    In this function we set the background
    Since the dino isn't actually moving we actually move the background on a loop

    '''
    def __init__(self, x):
        '''
        :param width: We set the width = to our global width variable
        :param height: We set the height = to out global height variable
        :param x: x value which changes so it = x
        :param y: y value which is always = to zero
        :param set_texture: texture function
        :param show: show function
        '''
        self.width = WIDTH
        self.height = HEIGHT
        self.X = x
        self.Y = 0
        self.set_texture()
        self.show()

    def update(self, dx):
        '''
        This function is used to update the moving images on a loop
        :param dx: the change in x
        :return:
        '''
        self.X += dx
        if self.X <= -WIDTH:
            self.X = WIDTH

    def show(self):
        '''
        shows the actual background
        '''
        screen.blit(self.texture, (self.X, self.Y))


    def set_texture(self):
        '''
        This one is used to make the background
        :param path: is the background its self, it = the path to the image
        The rest of the fuction is used to set it = to the game borders so its not to big or wide
        :return:
        '''
        path = os.path.join('assets/images/bg.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))



class Game:

    def __init__(self):
        self.bg = [BackGround(0, 0), BackGround(WIDTH, 0)]
        self.speed = 3

def main():

    game = Game()

    clock = pygame.time.Clock()

    while True:

        for bg in game.bg:
            bg.update(-game.speed)
            bg.show()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(80)
        pygame.display.update()



main()

