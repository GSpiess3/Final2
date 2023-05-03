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
    def __init__(self, x, y):
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
        self.Y = y
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

class Dino:

    def __init__(self):
        self.width = 44
        self.height = 44
        self.x = 10
        self.y = 80
        self.texture_num = 0
        self.dy = 3
        self.gravity = 1.2
        self.onground = True
        self.jumping = False
        self.jump_stop = 10
        self.falling = False
        self.fall_stop = self.y
        self.set_texture()
        self.show()

    def update(self, loops):
        '''
        resposnible for udating the dino
        '''
        #jumping
        if self.jumping:
            self.y -= self.dy
            if self.y <= self.jump_stop:
                self.fall()

        #falling
        elif self.falling:
            self.y += self.gravity * self.dy
            if self.y >= self.fall_stop:
                self.stop()

        #walking
        if self.onground and loops % 4 == 0:
            self.texture_num = (self.texture_num +1) % 3
            self.set_texture()

    def show(self):
        '''
        responsible for showing the dino
        '''
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        '''
        responsible for finding it converting it and making it usable
        '''

        path = os.path.join(f'assets/images/dino{self.texture_num}.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def jump(self):
        '''
        used to setting the booleans to the value we need while jumping
        :return:
        '''
        self.jumping = True
        self.onground = True

    def fall(self):
        '''
        booleans while falling
        :return:
        '''
        self.jumping = False
        self.falling = True

    def stop(self):
        '''
        booleans used to put you back on the ground
        :return:
        '''
        self.falling = False
        self.onground = True

class Cactus:

    def __init__(self, x):
        self.width = 34
        self.height = 44
        self.x = x
        self.y = 80
        self.set_texture()
        self.show()

    def update(self, dx):
        self.x += dx

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        path = os.path.join('assets/images/cactus.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

class Game:

    def __init__(self):
        self.bg = [BackGround(0, 0), BackGround(WIDTH, 0)]
        self.dino = Dino()
        self.obstactles = []
        self.speed = 3

    def tospawn(self, loops):
        return loops % 100 == 0


    def spawn_cactus(self):
        # list with cactus
        if len(self.obstactles) > 0:
            prev_cactus = self.obstactles[-1]
            # This allows enough room for our dino to land and jump between each cactus
            x = random.randint(prev_cactus.x + self.dino.width + 84, WIDTH + prev_cactus.x + self.dino.width + 84)


        #empty list
        else:
            x = random.randint(WIDTH + 100, 1000)

        #create new cactus
        cactus = Cactus(x)
        self.obstactles.append(cactus)


def main():

    #objects
    game = Game()
    dino = game.dino

    loops = 0

    clock = pygame.time.Clock()

    while True:

        loops += 1

        #----BG----
        for bg in game.bg:
            bg.update(-game.speed)
            bg.show()

        #---Dino---
        dino.update(loops)
        dino.show()

        #---cactus---

        if game.tospawn(loops):
            game.spawn_cactus()

        for cactus in game.obstactles:
            cactus.update(-game.speed)
            cactus.show()

        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    if dino.onground:
                        dino.jump()

        clock.tick(80)
        pygame.display.update()

main()

