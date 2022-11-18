import pygame
import time

W_WIDTH = 1024
W_HEIGHT = 600

START_TIME = time.time()

screen = pygame.display.set_mode([W_WIDTH, W_HEIGHT])
pygame.display.set_caption('Example')

def main():
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

if __name__ == "__main__":
    main()

