import pygame
from pygame.locals import *

class Background:
    surface = None

    def __init__(self):
        screen = pygame.display.get_surface()
        self.surface = pygame.Surface(screen.get_size()).convert()
        self.surface.fill((100, 50, 20))
        
    def draw(self, screen):
        screen.blit(self.surface, (0, 0))


class Game:
    run = True
    background = None

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([800, 600])
        self.background = Background()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.run = False

    def actors_update(self, dt):
        pass

    def actors_draw(self):
        self.background.draw(self.screen)

    def loop(self):
        dt = 40
        FPS = 1000 / dt
        clock = pygame.time.Clock()

        while self.run:
            clock.tick(FPS)
            self.handle_events()
            self.actors_update(dt)
            self.actors_draw()
            print('FPS: {0:.2f}'.format(clock.get_fps()))
            pygame.display.flip()


def main():
    game = Game()
    game.loop()

main()