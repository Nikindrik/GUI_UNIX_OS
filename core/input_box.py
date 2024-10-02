import pygame
from core import console
from core import emulator
from source.color import Color


console_output = console.ConsoleOutput
emulator_obj = emulator.Emulator

input_history = []
history_step = 0


class InputBox:
    def __init__(self, x, y, w, h, font_size, archive_path):  # Добавляем archive_path
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = (0, 0, 0)
        self.color_active = Color.anactice_white
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.font = pygame.font.Font(None, font_size)
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.min_w = w
        self.archive_path = archive_path  # Храним путь к архиву

    def handle_event(self, event):
        global history_step
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.text != '':
                        emulator.Emulator(self.archive_path).read_command(self.text)  # Передаем путь архива
                        self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pass
                else:
                    self.text += event.unicode
        self.txt_surface = self.font.render(self.text, True, Color.text_white)


    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)