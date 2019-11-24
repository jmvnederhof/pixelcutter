from main.python.reader import GcodeReader
from main.python.config import *
from tkinter import Tk, Canvas
import pygame
import time

reader = GcodeReader()
instructions = reader.read("../resources/octocat.gcode")
print("Instruction count: " + str(len(instructions)))
print("Lowest x: " + str(reader.lowest_x) + " highest x: " + str(reader.highest_x))
print("Lowest y: " + str(reader.lowest_y) + " highest y: " + str(reader.highest_y))


def close_window():
    global running
    running = False
    print("Window closed")


def print_bed_tkinter():
    tk = Tk()
    tk.title(title)
    tk.resizable(0, 0)
    tk.protocol("WM_DELETE_WINDOW", close_window)
    tk.wm_attributes("-topmost", 1)
    canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
    canvas.pack()
    tk.update()


def print_bed_pygame():
    screen.fill(color_screen)
    surface.fill(color_screen)
    pygame.display.set_caption(title)


print_bed_offset_x = -1.0 * reader.lowest_x + 10.0
print_bed_offset_y = -1.0 * reader.lowest_y + 10.0

screen = pygame.display.set_mode((width, height))
surface = pygame.surface.Surface((width, height))
print_bed_pygame()

if instructions[0].y is not None:
    pygame.draw.line(screen, color_line, (0, int(instructions[0].y * scale + print_bed_offset_y)),
                     (500, int(instructions[0].y * scale + print_bed_offset_y)))
if instructions[0].x is not None:
    pygame.draw.line(screen, color_line, (int(instructions[0].x * scale + print_bed_offset_x), 0),
                     (int(instructions[0].x * scale + print_bed_offset_x), 400))


def execute_instruction(current_instruction, new_instruction):
    if new_instruction.z is not None:
        print(str(new_instruction.z))

    if new_instruction.x is not None and new_instruction.y is not None and current_instruction.x is not None and \
            current_instruction.y is not None:
        pygame.draw.line(surface, color_line,
                         (print_bed_offset_x + scale * current_instruction.x,
                          print_bed_offset_y + scale * current_instruction.y),
                         (print_bed_offset_x + scale * new_instruction.x,
                          print_bed_offset_y + scale * new_instruction.y))

        if new_instruction.y is not None:
            pygame.draw.line(screen, color_line, (0, new_instruction.y * scale + print_bed_offset_y),
                             (width, new_instruction.y * scale + print_bed_offset_y))
        if new_instruction.x is not None:
            pygame.draw.line(screen, color_line, (new_instruction.x * scale + print_bed_offset_x, 0),
                             (new_instruction.x * scale + print_bed_offset_x, height))


instruction_index = 0
running = True

while 1:
    if not running:
        break

    if instruction_index < len(instructions):
        current_instruction_index = instruction_index
        instruction_index += 1
        new_instruction_index = instruction_index
        execute_instruction(instructions[current_instruction_index], instructions[new_instruction_index])

    pygame.display.update()
    pygame.display.flip()
    screen.blit(surface, (0, 0))
    time.sleep(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
