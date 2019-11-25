from main.python.reader import GCodeReader
from main.python.pixel_cutter import PixelCutter
import pygame
import time

instructions_per_second = 20
speed = 1 / instructions_per_second


def run():
    pixel_cutter = PixelCutter(GCodeReader("../resources/octocat.gcode"))
    running = True
    while 1:
        pixel_cutter.execute_next_instruction()
        time.sleep(speed)

        if not running:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


run()
