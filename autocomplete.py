import fnmatch
import functools
import re
import sys
import time

from terminal import Terminal
from tablefmt import Table

class Input:
    def __init__(self, options=list(), completion_mode=None):
        self.term = Terminal()

        self.options = options
        self.completion_mode = completion_mode # "cycle", "show_matches"
        self.completion_char = "\t"
        self.completion_state = 0
        self.history = list()

    def register_handler(self, name, callback):
        self.handlers[name] = callback

    def read_token(self, prompt):
        line = ""
        guess = ""
        history_pos = -1
        insert_mode = True
        col = 1

        self.print(prompt)

        while True:
            # find token
            token = ""
            s, e = 0, 0
            # FIXME: no token when at 0, 0
            for match in re.finditer(r"([^ ]+| )", line):
                s, e = match.span() # starts at zero
                if col - 1 >= s and col - 1 <= e:
                    token = line[s:e]
                    break

            # focus token
            # self.term.clear_line(2)
            # self.term.set_column(1)
            # self.print(line[0:s])
            # self.term.reverse()
            # self.print(token)
            # self.term.off()
            # self.print(line[e:])
            # self.term.set_column(col)

            # print status
            self.term.right(len(line))
            self.print("\n")
            self.term.clear_line()
            self.print(f"Column {col}, Token {token}")
            self.term.up()
            self.term.set_column(len(prompt) + col)

            c = self.term.read_char()

            if self.completion_mode:
                # TODO: wait for another enter
                # TODO: make token-based extensions
                if c is self.completion_char:
                    token, guess = self.complete(token)
                    self.term.clear_line(1)
                    self.term.set_column(len(prompt) + 1)
                    self.print(token)

                    self.term.reverse()
                    self.print(guess)
                    self.term.off()
                    self.completion_state += 1
                    continue
                elif self.completion_state and c is "\b" and guess:
                    self.term.left(len(guess)-1)
                    self.term.clear_line()
                    self.completion_state = 0
                elif self.completion_state:
                    token += guess # FIXME: or replace
                    if guess:
                        self.term.left(len(guess))
                        self.print(guess)
                    self.completion_state = 0
                    guess = ""

            if c is "left":
                if col > 1:
                    self.term.left()
                    col -= 1
            elif c is "right":
                if col < len(line) + 1:
                    self.term.right()
                    col += 1
            elif c is "home":
                self.term.set_column(len(prompt) + 1)
                col = 1
            elif c is "end":
                self.term.set_column(len(prompt) + len(line) + 1)
                col = len(line) + 1
            elif c is "del":
                line = line[:col-1] + line[col:]
                self.term.clear_line(0)
                self.print(line[col-1:])
                self.term.set_column(len(prompt) + col)
            elif c is "ins":
                insert_mode = not insert_mode
            elif c is "up":
                if history_pos < len(self.history) - 1:
                    history_pos += 1
                    line = self.history[history_pos]
                    self.term.set_column(len(prompt) + 1)
                    self.term.clear_line(0)
                    self.print(line)
            elif c is "down":
                if history_pos > 0:
                    history_pos -= 1
                    line = self.history[history_pos]
                    self.term.set_column(len(prompt) + 1)
                    self.term.clear_line(0)
                    self.print(line)
            elif c is "jump_left":
                self.term.set_column(len(prompt) + s + 1)
                col = s + 1
            elif c is "jump_right":
                self.term.set_column(len(prompt) + e + 1)
                col = e + 1
            elif c in ("pgup", "pgdn"):
                pass
            elif c is "\b":
                if col <= 1:
                    continue
                line = line[:col-2] + line[col-1:]
                self.term.left(1)
                self.term.clear_line()
                self.print(line[col-2:])
                self.term.set_column(len(prompt) + col - 1)
                col -= 1
            elif c in  ["\n", "\r"]:
                # TODO: treat r differently?
                # TODO: go beyond status line
                self.term.next_line()
                self.term.set_column(len(prompt) + len(line) + 1)
                self.print(c)
                self.history.insert(0, line)
                col = 1
                return line
            else:
                if insert_mode:
                    line = line[:col-1] + c + line[col-1:]
                    # self.term.clear_line(0)
                    self.print(line[col-1:])
                    col += 1
                else:
                    line = line[:col-1] + c + line[col:]
                    self.print(c)
                    col += 1

    def complete(self, token):
        matches = self.match(token)
        if len(matches) == 0:
            return token, ""
        elif len(matches) == 1:
            return matches[0], ""

        while True:
            expansion = matches[0][:len(token)+1]
            if len(self.match(expansion)) < len(matches):
                break
            token = expansion
            if token is matches[0]:
                break

        if self.completion_mode is "show_matches":
            print("\nDid you mean:")
            t = Table()
            t.feed_list(matches)
            t.print()
            guess = ""
        elif self.completion_mode is "cycle":
            guess = matches[self.completion_state % len(matches)][len(token):]

        return token, guess

    def match(self, token):
        return fnmatch.filter(self.options, token + "*")

    def print(self, msg):
        print(msg, end="", flush=True)


def demo():
    options = ["Robert", "Jimmy", "John", "John Paul"]
    c = Input(options, completion_mode="cycle")
    inp = ""
    while inp != "exit":
        inp = c.read_token("\u2665 ")
        print("Input:", inp)

if __name__ == "__main__":
    demo()

    # print(Terminal().get_position())
    exit()

    line = "H l"
    col = 1
    for match in re.finditer(r"([^ ]+| )", line):
        # print(line, match)
        # print(line)
        s, e = match.span()
        print(s, e)
        if col >= s + 1 and col <= e + 1:
            token = line[s:e]
            print(token)