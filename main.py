import os
import pygame
from pygame.locals import *

IMAGES_PATH = os.path.join(".", "images")

class Background:
    image = None

    def __init__(self):
        screen = pygame.display.get_surface()
        self.image = pygame.Surface(screen.get_size()).convert()
        self.image.fill((100, 50, 20))
        
    def draw(self, screen):
        screen.blit(self.image, (0, 0))


class GameObject(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.set_position(position)

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
        GameObject.__init__(self, (0, 0))
        screen = pygame.display.get_surface()
        screen_size = screen.get_size()
        self.image = pygame.Surface((screen_size[0]/10, screen_size[1]/30)).convert()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.bottom = 600
        self.rect.centerx = 400

    def update(self, dt):
        self.rect.centerx += 25
        if self.rect.left > pygame.display.get_surface().get_size()[0]:
            self.rect.right = 0

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