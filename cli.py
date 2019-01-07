import time

from tablefmt import Table
from autocomplete import Input

class CLI:
    def __init__(self, prompt="\x1b[31m\u2764\x1b[m ", intro="Command Line Interface"):
        self.prompt = prompt
        self.intro = intro
        self.readline = Input(options=["Hello", "Hola"], completion_mode="cycle")

    def run(self):
        if self.intro:
            print(self.intro)
        while True:
            self.query()

    def query(self):
        """Query input, pass """
        inp = self.input()

        # TODO: Handle no input
        # TODO: Handle wrong input
        # TODO: extend to multicharacter names
        cmd = inp[0]
        args = inp[1:].strip()

        try:
            fun = getattr(self, "on_" + cmd)
        except:
            fun = self.on_h
            print("Invalid command!")
        fun(*args.split())

    def input(self):
        # TODO: add nonblocking input
        # return input(self.prompt)
        return self.readline.read_token()

    def on_h(self, *args):
        """Show help."""
        table = Table(colsep=":")
        for name in dir(self):
            if name[:3] == "on_":
                cmd = name[3:]
                # get first line of docstring
                expl = getattr(self, name).__doc__.splitlines()[0].rstrip(".")
                table.append(cmd, expl)
        print()
        table.print()
        print()

    def on_q(self, *args):
        """Quit program."""
        exit()

if __name__ == "__main__":
    CLI().run()