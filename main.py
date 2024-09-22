import pygame
import sys
import input_box
import console
from color import Color as Color


pygame.init()

icon = pygame.image.load('source/img/UNIX_GUI_icon.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((650, 500))
pygame.display.set_caption('UNIX GUI emulation')

def alert_detah():
    pygame.quit()
    sys.exit()

def main():
    clock = pygame.time.Clock()
    console_output = console.ConsoleOutput(25, 18, 90, 600, 375)
    inputbox = input_box.InputBox(10, 50, 615, 30, 25)
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            inputbox.handle_event(event)

        screen.fill(Color.graphite_grey)
        console_output.draw(screen)
        inputbox.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()