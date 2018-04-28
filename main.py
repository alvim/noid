import pygame


class Game:
    run = True

    def loop(self):
        while self.run:
            print('Running...')



def main():
    game = Game()
    game.loop()

main()