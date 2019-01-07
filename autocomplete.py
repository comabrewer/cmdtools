import fnmatch
import functools
import msvcrt
import sys

from terminal import Terminal
from tablefmt import Table

class Input:
    def __init__(self, options=list(), completion_mode=None):
        self.term = Terminal()

        self.options = options
        self.completion_mode = completion_mode # "cycle", "show_matches"
        self.completion_char = "\t"
        self.completion_state = 0

    def register_handler(self, name, callback):
        self.handlers[name] = callback

    def read_token(self, prompt):
        token = ""
        guess = ""
        insert_mode = False

        while True:
            c = self.term.read_char()

            if self.completion_mode:
                if c is self.completion_char:
                    # based on guess or on token? Update guess or token?
                    token, guess = self.complete(token)
                    self.term.clear_line(1)
                    self.term.set_column(0)
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
                    token += guess
                    if guess:
                        self.term.left(len(guess))
                        self.print(guess)
                    self.completion_state = 0
                    guess = ""

            if c is "left":
                self.term.left(1)
            elif c is "right":
                _, col = self.term.get_position()
                if col <= len(token):
                    self.term.right(1)
            elif c is "home":
                self.term.set_column(0)
            elif c is "end":
                self.term.set_column(len(token) + 1)
            elif c is "del":
                row, col = self.term.get_position()
                token = token[:col-1] + token[col:]
                self.term.clear_line(0)
                self.print(token[col-1:])
                self.term.set_column(col)
            elif c is "ins":
                insert_mode = not insert_mode
            elif c in ("up", "down", "pgup", "pgdn"):
                pass
            elif c is "\b":
                _, col = self.term.get_position()
                token = token[:col-2] + token[col-1:]
                self.term.left(1)
                self.term.clear_line()
                self.print(token[col-2:])
                self.term.set_column(col - 1)
            elif c in  ["\n", "\r"]:
                # TODO: treat r differently?
                print()
                return token
            else:
                _, col = self.term.get_position()
                if insert_mode:
                    token = token[:col-1] + c + token[col-1:]
                    self.term.clear_line()
                    self.print(token[col-1:])
                    self.term.set_column(col+1)
                else:
                    token = token[:col-1] + c + token[col:]
                    self.print(c)

    def read_line():
        """TODO: similar to read_token, but has notion of multiple tokens in line.

        This enables token-based completion. """
        pass

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
    c = Input(options, completion_mode="show_matches")
    inp = c.read_token()
    print("Input:", inp)

if __name__ == "__main__":
    demo()
