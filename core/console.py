import pygame
from source.color import Color


text_list = []
text_animation_step = 1
text_animation_y = 20

class ConsoleOutput:
    def __init__(self, font_size, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.Font(None, font_size)
        self.line_height = self.font.get_height()

    def draw(self, screen):
        pygame.draw.rect(screen, Color.black, self.rect, 2)

        if len(text_list) > 18:
            text_list.pop(0)

        for i in range(len(text_list)):
            img = self.font.render(text_list[i], True, Color.text_white)
            screen.blit(img, (30, 100 + 20 * i))

        img = self.font.render("Type command", True, Color.text_white)
        screen.blit(img, (225, text_animation_y))