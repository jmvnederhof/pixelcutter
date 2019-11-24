class Instruction:
    def __init__(self, line_of_gcode):
        self._g = self.parse_code_id(line_of_gcode, "G")
        self._x = self.parse_code_id(line_of_gcode, "X")
        self._y = self.parse_code_id(line_of_gcode, "Y")
        self._e = self.parse_code_id(line_of_gcode, "E")
        self._z = self.parse_code_id(line_of_gcode, "Z")
        self._f = self.parse_code_id(line_of_gcode, "F")

    def parse_code_id(self, line_of_gcode, code_id):
        if line_of_gcode.__contains__(code_id):
            code = line_of_gcode[line_of_gcode.index(code_id):]
            if code.__contains__(' '):
                if self.is_float(code[1:code.index(' ')]):
                    return float(code[1:code.index(' ')])
            elif code.__contains__('\n'):
                if self.is_float(code[1:code.index('\n')]):
                    return float(code[1:code.index('\n')])
        else:
            return None

    @staticmethod
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    @property
    def g(self):
        return self._g

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def e(self):
        return self._e

    @property
    def z(self):
        return self._z

    @property
    def f(self):
        return self._f
