import pygame
import time

W_WIDTH = 1024
W_HEIGHT = 600

START_TIME = time.time()

screen = pygame.display.set_mode([W_WIDTH, W_HEIGHT])
pygame.display.set_caption('Example')

def main():
    while True:
        pygame.draw.ellipse(screen, (148, 0, 211), [400, 100, 300, 400], 5)
        pygame.draw.circle(screen, "blue", [480, 270], 20)
        pygame.draw.circle(screen, "blue", [630, 270], 20)
        pygame.draw.arc(screen, "red", [480, 300, 150, 125], 3.14, 0, 5)


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

if __name__ == "__main__":
    main()

