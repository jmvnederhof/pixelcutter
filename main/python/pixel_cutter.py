from main.python.config import *
import pygame


class PixelCutter:
    def __init__(self, reader):
        self.__reader = reader
        self.__instructions = reader.read()
        self.__screen = pygame.display.set_mode((width, height))
        self.__surface = pygame.surface.Surface((width, height))
        self.__print_bed_offset_x = 0
        self.__print_bed_offset_y = 0
        self.__new_instruction_index = 0
        self.setup_surface()
        self.__instruction_index = self.__next_valid_instruction(self.__instructions, 0)

    def setup_surface(self):
        self.__print_bed_offset_x = -1.0 * self.__reader.lowest_x + 50.0
        self.__print_bed_offset_y = -1.0 * self.__reader.lowest_y + 50.0
        self.__screen = pygame.display.set_mode((width, height))
        self.__surface = pygame.surface.Surface((width, height))
        self.__screen.fill(color_screen)
        self.__surface.fill(color_screen)
        pygame.display.set_caption(title)

    def __next_valid_instruction(self, instructions, instruction_index):
        while instruction_index < len(instructions):
            if instructions[instruction_index].g == 1 and instructions[instruction_index].x is not None:
                return instruction_index
            instruction_index += 1

    def execute_next_instruction(self):
        if self.__instruction_index < len(self.__instructions):
            current_instruction_index = self.__instruction_index
            self.__instruction_index += 1
            self.__new_instruction_index = self.__next_valid_instruction(self.__instructions, self.__instruction_index)
            if self.__new_instruction_index is not None:
                self.__execute_instruction(self.__instructions[current_instruction_index],
                                           self.__instructions[self.__new_instruction_index])
            else:
                self.__screen.blit(self.__surface, (0, 0))
                self.__draw_height_indicator(99.9)
                self.__draw_progress_indicator()
                pygame.display.flip()

    def __execute_instruction(self, current_instruction, new_instruction):
        self.__draw_filament(current_instruction, new_instruction)
        self.__draw_xy_axis(new_instruction)
        self.__draw_height_indicator(new_instruction.z)
        self.__draw_progress_indicator()
        pygame.display.flip()

    def __draw_filament(self, current_instruction, new_instruction):
        if new_instruction.x is not None and new_instruction.y is not None and current_instruction.x is not None and \
                current_instruction.y is not None and new_instruction.f is not None and new_instruction.f < 1600:
            pygame.draw.aaline(self.__surface, color_line,
                               (self.__print_bed_offset_x + scale * current_instruction.x,
                                self.__print_bed_offset_y + scale * current_instruction.y),
                               (self.__print_bed_offset_x + scale * new_instruction.x,
                                self.__print_bed_offset_y + scale * new_instruction.y), 2)

            self.__screen.blit(self.__surface, (0, 0))

    def __draw_xy_axis(self, current_instruction):
        if current_instruction.y is not None:
            pygame.draw.line(self.__screen, color_line,
                             (0, current_instruction.y * scale + self.__print_bed_offset_y),
                             (width, current_instruction.y * scale + self.__print_bed_offset_y))
        if current_instruction.x is not None:
            pygame.draw.line(self.__screen, color_line,
                             (current_instruction.x * scale + self.__print_bed_offset_x, 0),
                             (current_instruction.x * scale + self.__print_bed_offset_x, height))

    def __draw_height_indicator(self, height_value):
        if height_value is not None:
            pygame.font.init()
            font = pygame.font.Font(pygame.font.get_default_font(), font_size)
            elevation_text = font.render("Z:" + str(height_value), True, color_line)
            self.__screen.blit(elevation_text, (10, 10))

    def __draw_progress_indicator(self):
        pygame.font.init()
        font = pygame.font.Font(pygame.font.get_default_font(), font_size)
        complete_pct = round(self.__instruction_index / len(self.__instructions) * 100, 1)
        completion_status = "complete"
        if complete_pct < 99.99:
            completion_status = str(complete_pct) + "%"

        progress_text = font.render(
            "Progress:" + completion_status, True,
            color_line)
        self.__screen.blit(progress_text, (90, 10))
