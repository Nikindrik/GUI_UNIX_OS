import pygame
import sys
from core import input_box
from core import console
from source.color import Color as Color
import os
import argparse
from core import emulator

pygame.init()

icon = pygame.image.load('source/img/UNIX_GUI_icon.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((650, 500))
pygame.display.set_caption('UNIX GUI emulation')

def alert_detah():
    pygame.quit()
    sys.exit()

def execute_startup_script(script_path, archive_path):
    if os.path.exists(script_path):
        with open(script_path, 'r') as script_file:
            commands = script_file.readlines()
            for command in commands:
                command = command.strip()
                if command:
                    console.text_list.append(f"Executing command: {command}")
                    emulator.Emulator(archive_path).read_command(command)
    else:
        console.text_list.append(f"ERROR: Startup script {script_path} not found.")

def main(user_name, archive_path, script_path):
    if not os.path.exists(archive_path):
        console.text_list.append(f"ERROR: Archive {archive_path} not found.")
        return

    clock = pygame.time.Clock()
    console_output = console.ConsoleOutput(25, 18, 90, 600, 375)
    inputbox = input_box.InputBox(10, 50, 615, 30, 25, archive_path)  # Передаем путь к архиву
    done = False

    execute_startup_script(script_path, archive_path)

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
    parser = argparse.ArgumentParser(description="UNIX GUI Emulation")
    parser.add_argument('--user', required=True, help="User name for console prompt")
    parser.add_argument('--archive', required=True, help="Path to virtual filesystem archive")
    parser.add_argument('--script', required=True, help="Path to startup script")

    args = parser.parse_args()

    main(args.user, args.archive, args.script)