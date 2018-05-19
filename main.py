import os
import sys
import getopt
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
    speed = (0, 0)

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

    def go_left(self):
        self.speed = (-5, 0)

    def go_right(self):
        self.speed = (5, 0)

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

class Ball(GameObject):
    speed = (8, 8)

    def __init__(self):
        GameObject.__init__(self, (0, 0))
        self.image = pygame.Surface((10, 10)).convert()
        pygame.draw.circle(self.image, (0, 0, 255), (5, 5), 5, 0)
        # self.image.fill((255, 255, 255))
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

        if self.rect.top > self.screen_size[1]:
            self.rect.bottom = 0
            self.position = self.rect.center
        elif self.rect.bottom < 0:
            self.rect.top = self.screen_size[1]
            self.position = self.rect.center

    def update(self, dt):
        self.set_position((self.position[0] + self.speed[0], self.position[1] + self.speed[1]))
        self.rect.center = self.position


class Game:
    run = True
    background = None
    balls_list = pygame.sprite.Group()
    all_sprites = pygame.sprite.RenderUpdates()

    def __init__(self, size, fullscreen):
        pygame.init()
        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN
        self.screen = pygame.display.set_mode(size, flags)
        self.background = Background()

    def handle_events(self):
        balls_hitted = pygame.sprite.spritecollide(self.player, self.balls_list, False)
        for ball in balls_hitted:
            ball.set_speed((ball.speed[0], ball.speed[1] * -1))

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            if event.type == QUIT:
                self.run = False
            elif event.type == KEYDOWN:
                if keys[K_LEFT]:
                    self.player.go_left()
                elif keys[K_RIGHT]:
                    self.player.go_right()
            elif event.type == KEYUP:
                if not keys[K_RIGHT] and not keys[K_LEFT]:
                    self.player.set_speed((0, 0))


    def actors_update(self, dt):
        self.all_sprites.update(dt)

    def actors_draw(self):
        self.all_sprites.clear(self.screen, self.background.image)
        rectlist = self.all_sprites.draw(self.screen)
        pygame.display.update(rectlist)

    def play(self):
        self.player = Player()
        self.ball = Ball()
        self.balls_list.add(self.ball)
        self.all_sprites.add(self.player, self.ball)

    def loop(self):
        dt = 10
        FPS = 1000 / dt
        clock = pygame.time.Clock()
        self.background.draw(self.screen)
        pygame.display.update()
        self.play()

        while self.run:
            clock.tick(FPS)
            self.handle_events()
            self.actors_update(dt)
            self.actors_draw()
            # print('FPS: {0:.2f}'.format(clock.get_fps()))

def parse_opts( argv ):
    try:
        opts, args = getopt.gnu_getopt( argv[ 1 : ],
                                        "hfr:",
                                        [ "help",
                                          "fullscreen",
                                          "resolution=" ] )
    except getopt.GetoptError:
        usage()
        sys.exit( 2 )

    options = {
        "fullscreen":  False,
        "resolution": ( 640, 480 ),
    }

    for o, a in opts:
        if o in ( "-f", "--fullscreen" ):
            options[ "fullscreen" ] = True
        elif o in ( "-h", "--help" ):
            usage()
            sys.exit( 0 )
        elif o in ( "-r", "--resolution" ):
            a = a.lower()
            r = a.split( "x" )
            if len( r ) == 2:
                options[ "resolution" ] = r
                continue

            r = a.split( "," )
            if len( r ) == 2:
                options[ "resolution" ] = r
                continue

            r = a.split( ":" )
            if len( r ) == 2:
                options[ "resolution" ] = r
                continue

    r = options[ "resolution" ]
    options[ "resolution" ] = [ int( r[ 0 ] ), int( r[ 1 ] ) ]
    return options

def main(argv):
    options = parse_opts(argv)
    game = Game(options["resolution"], options["fullscreen"])
    game.loop()

main(sys.argv)