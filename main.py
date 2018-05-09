import os
import pygame
from pygame.locals import *
from math import ceil

IMAGES_PATH = os.path.join(".", "images")

class Background:
    image = None

    def __init__(self):
        screen_size = pygame.display.get_surface().get_size()
        background = pygame.Surface(screen_size)
        image = pygame.image.load(os.path.join(IMAGES_PATH, 'bg_universe.jpg')).convert()
        image_size = image.get_size()

        for i in range(ceil(screen_size[0] / image_size[0])):
            for j in range(ceil(screen_size[1] / image_size[1])):
                background.blit(image, (i * image_size[0], j * image_size[1]))

        self.image = background
        
    def draw(self, screen):
        screen.blit(self.image, (0, 0))


class GameObject(pygame.sprite.Sprite):
    speed = (2, 0)

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.position = position
        self.screen_size = screen.get_size()

    def update(self):
        pass

    # def draw(self, screen):
    #     screen.blit(self.image, self.position)

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def get_position(self):
        return self.position
    
    def set_position(self, position):
        self.position = position


class Player(GameObject):
    image = None
    rect = None

    def __init__(self):
        GameObject.__init__(self, (400, 300))
        self.image = pygame.Surface((self.screen_size[0]/10, self.screen_size[1]/30)).convert()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.position


    def set_position(self, position):
        self.position = position
        if self.rect.left > self.screen_size[0]:
            self.rect.right = 0
            self.position = self.rect.center
        elif self.rect.right < 0:
            self.rect.left = self.screen_size[0]
            self.position = self.rect.center

    def update(self, dt):
        self.set_position((self.position[0] + self.speed[0], self.position[1] + self.speed[1]))
        self.rect.center = self.position

class Game:
    run = True
    background = None
    all_sprites = pygame.sprite.RenderUpdates()

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([800, 600])
        self.background = Background()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.run = False

    def actors_update(self, dt):
        self.all_sprites.update(dt)

    def actors_draw(self):
        self.all_sprites.clear(self.screen, self.background.image)
        rectlist = self.all_sprites.draw(self.screen)
        pygame.display.update(rectlist)

    def play(self):
        player = Player()
        self.all_sprites.add(player)

    def loop(self):
        dt = 40
        FPS = 1000 / dt
        clock = pygame.time.Clock()
        self.background.draw(self.screen)
        pygame.display.update()
        self.play()

        print(self.screen)

        while self.run:
            clock.tick(FPS)
            self.handle_events()
            self.actors_update(dt)
            self.actors_draw()
            # print('FPS: {0:.2f}'.format(clock.get_fps()))


def main():
    game = Game()
    game.loop()

main()