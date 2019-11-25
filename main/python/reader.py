from main.python.model import Instruction


class GCodeReader:
    def __init__(self, path_to_gcode):
        self.highest_x = 0
        self.highest_y = 0
        self.lowest_x = 0
        self.lowest_y = 0
        self.__path_to_gcode = path_to_gcode

    def read(self):
        instructions = []
        with open(self.__path_to_gcode, "r") as fp:
            for line in fp:
                instruction = Instruction(line)
                instructions.append(instruction)
                self.detect_and_store_extremes(instruction)
        return instructions

    def detect_and_store_extremes(self, instruction):
        if instruction.x is not None:
            if instruction.x < self.lowest_x:
                self.lowest_x = instruction.y
            if instruction.x > self.highest_x:
                self.highest_x = instruction.y
        if instruction.y is not None:
            if instruction.y < self.lowest_y:
                self.lowest_y = instruction.y
            if instruction.y > self.highest_y:
                self.highest_y = instruction.y
