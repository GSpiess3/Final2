# base file
import os
import sys
import math
import random
from typing import Union
import pygame
from pygame import Surface, SurfaceType

WIDTH = 623
HEIGHT = 150


pygame.init()
pygame.mixer.init()
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
        self.set_sound()
        self.show()

    def update(self, loops):
        '''
        resposnible for udating the dino
        '''
        # jumping
        if self.jumping:
            self.y -= self.dy
            if self.y <= self.jump_stop:
                self.fall()

        # falling
        elif self.falling:
            self.y += self.gravity * self.dy
            if self.y >= self.fall_stop:
                self.stop()

        # walking
        if self.onground and loops % 4 == 0:
            self.texture_num = (self.texture_num + 1) % 3
            self.set_texture()

    def set_sound(self):
        path = os.path.join('assets/sounds/jump.wav')
        self.sound = pygame.mixer.Sound(path)

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
        self.sound.play()
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

class Collision:

    def between(self, obj1, obj2):
        distance = math.sqrt((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2)
        return distance < 35

class Score:

    def __init__(self, hs = 0):

        self.hs = self.load_high_score() if hs == 0 else hs
        self.act = 0
        self.font = pygame.font.SysFont('monospace', 18)
        self.color = (0, 0, 0)
        self.set_sound()
        self.show()

    def load_high_score(self):
        try:
            with open('score.txt', 'r') as file:
                content = file.read().strip()
                if content:
                    return int(content)
        except (FileNotFoundError, ValueError):
            print("File not found error")
        return 0

    def save_high_score(self, hs):
        with open('score.txt', 'w') as file:
            file.write(str(hs))

    def update_high_score(self, current_score):
        if current_score > self.hs:
            self.hs = current_score
            self.save_high_score(self.hs)


    def update(self, loops):
        self.act = loops // 10
        self.check_hs()
        self.check_sound()

    def show(self):
        self.lbl = self.font.render(f'HI {self.hs} {self.act}', 1, self.color)
        lbl_width = self.lbl.get_rect().width
        screen.blit(self.lbl, (WIDTH - lbl_width - 10, 10))

    def set_sound(self):
        path = os.path.join('assets/sounds/point.wav')
        self.sound = pygame.mixer.Sound(path)


    def check_hs(self):
        if self.act >= self.hs:
            self.hs = self.act


    def check_sound(self):
        if self.act % 100 == 0 and self.act != 0:
            self.sound.play()

class Game:

    def __init__(self, hs=0):
        self.bg = [BackGround(0, 0), BackGround(WIDTH, 0)]
        self.dino = Dino()
        self.obstactles = []
        self.collision = Collision()
        self.score = Score(hs)
        self.speed = 3
        self.start_label()
        screen.blit(self.start_big_lbl, (WIDTH / 2 - self.start_big_lbl.get_width() // 2, HEIGHT // 4))
        screen.blit(self.start_small_lbl, (WIDTH // 2 - self.start_small_lbl.get_width() // 2, HEIGHT // 2))
        self.playing = False
        self.set_sound()
        self.set_labels()


    def start_label(self):
        big_font = pygame.font.SysFont('monospace', 24, bold=True)
        small_font = pygame.font.SysFont('monospace', 18)
        self.start_big_lbl = big_font.render(f'D I N O  G A M E', 1, (0, 0, 0))
        self.start_small_lbl = small_font.render(f'Press space to start/play', 1, (0, 0, 0))
    def set_labels(self):
        big_font = pygame.font.SysFont('monospace', 24, bold=True)
        small_font = pygame.font.SysFont('monospace', 18)
        self.reset_big_lbl = big_font.render(f'G A M E  O V E R', 1, (0, 0, 0))
        self.reset_small_lbl = small_font.render(f'Press r to restart', 1, (0, 0, 0))


    def set_sound(self):
        path = os.path.join('assets/sounds/die.wav')
        self.sound = pygame.mixer.Sound(path)
    def start(self):
        self.playing = True

    def over(self):
        self.sound.play()
        screen.blit(self.reset_big_lbl, (WIDTH/2 - self.reset_big_lbl.get_width() // 2, HEIGHT // 4))
        screen.blit(self.reset_small_lbl, (WIDTH // 2 - self.reset_small_lbl.get_width() // 2, HEIGHT// 2))
        self.score.save_high_score(self.score.act)
        self.playing = False

    def tospawn(self, loops):
        return loops % 100 == 0

    def spawn_cactus(self):
        '''
        will spawn cactus
        :return:
        '''
        # list with cactus
        if len(self.obstactles) > 0:
            prev_cactus = self.obstactles[-1]
            # This allows enough room for our dino to land and jump between each cactus
            x = random.randint(prev_cactus.x + self.dino.width + 84, WIDTH + prev_cactus.x + self.dino.width + 84)


        # empty list
        else:
            x = random.randint(WIDTH + 100, 1000)

        # create new cactus
        cactus = Cactus(x)
        self.obstactles.append(cactus)

    def restart(self):
        '''
        this function will restart the game if the r is hit
        :return:
        '''
        self.score.save_high_score(self.score.act)
        self.__init__(hs=self.score.hs)

def main():
    # objects
    game = Game()
    dino = game.dino

    #variables
    loops = 0
    clock = pygame.time.Clock()
    over = False


    while True:

        if game.playing:

            loops += 1

            # ----BG----
            for bg in game.bg:
                bg.update(-game.speed)
                bg.show()

            # ---Dino---
            dino.update(loops)
            dino.show()

            # ---cactus---

            if game.tospawn(loops):
                game.spawn_cactus()

            for cactus in game.obstactles:
                cactus.update(-game.speed)
                cactus.show()

                # ---Collision---
                if game.collision.between(dino, cactus):
                    over = True

            if over:
                game.score.update_high_score(game.score.act)
                game.over()

            #---Score---
            game.score.update(loops)
            game.score.show()

        # events and keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    if not over:
                        if dino.onground:
                            dino.jump()
                        if not game.playing:
                            game.start()

                if event.key == pygame.K_r:
                    game.restart()
                    dino = game.dino
                    loops = 0
                    over = False

        clock.tick(80)
        pygame.display.update()


if __name__ == '__main__':
    main()
