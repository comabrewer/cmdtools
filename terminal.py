import functools
import msvcrt
import sys


class Terminal:
    esc = "\x1b"
    csi = esc + "["

    special_inp_chars = {
        "G": "home",
        "H": "up",
        "I": "pgup",
        "K": "left",
        "M": "right",
        "O": "end",
        "P": "down",
        "Q": "pgdn",
        "R": "ins",
        "S": "del",
    }

    ansi_ctrl_codes = {
        "up": "A",
        "down": "B",
        "right": "C",
        "left": "D",
        "next_line": "E",
        "prev_line": "F",
        "set_column": "G",
        "set_position": "H",
        "clear_screen": "J", # 0: end, 1: start, 2: full
        "clear_line": "K",
        "save_position": "s",
        "restore_position": "u",
        "graphics": "m",
        "query_position": "6n",
        "show_cursor": "?25h",
        "hide_cursor": "?25l"
    }

    ansi_graphic_codes = {
        "off": 0,
        "bold": 1,
        "underscore": 4,
        "blink": 5,
        "reverse": 7,
        "concealed": 8,
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
        "bg_black": 40,
        "bg_red": 41,
        "bg_green": 42,
        "bg_yellow": 43,
        "bg_blue": 44,
        "bg_magenta": 45,
        "bg_cyan": 46,
        "bg_white": 47,
    }

    def __init__(self):
        for name in self.ansi_ctrl_codes:
            setattr(self, f"{name}", functools.partial(self.write_ctrl_seq, name))
            setattr(self, f"get_seq_{name}", functools.partial(self.get_ctrl_seq, name))
        for name, code in self.ansi_graphic_codes.items():
            setattr(self, f"{name}", functools.partial(self.write_ctrl_seq, "graphics", code))
            setattr(self, f"get_seq_{name}", functools.partial(self.get_ctrl_seq, "graphics", code))

    def read_char(self):
        """Reads single character from the command line.

        If the character is a known control character, returns a string alias.
        Otherwise returns the character as unicode string of length 1.

        Works only on MS Windows.

        """
        # TODO: catch ctrl + C, Z, etc... use kbhit?
        c = msvcrt.getwch()
        if c in ("\xe0", "\x00"):
            c = msvcrt.getwch()
            return self.special_inp_chars[c]
        return c

    def get_ctrl_seq(self, name, *args):
        """Get ANSI escape sequence."""
        params = ";".join([str(arg) for arg in args])
        seq = "{}{}{}".format(self.csi, params, self.ansi_ctrl_codes[name])
        return seq

    def write_ctrl_seq(self, name, *args, flush=True, f=sys.stdout):
        """Write ANSI escape sequence to file descriptor."""
        seq = self.get_ctrl_seq(name, *args)
        print(seq, end="", flush=flush, file=f)

    def get_position(self):
        """Get current cursor position."""
        self.query_position()
        c = ""
        buf = ""
        while c != "R":
            c = self.read_char()
            buf += c
        return tuple([int(val) for val in buf[len(self.csi):-1].split(";")])


if __name__ == "__main__":
    pass