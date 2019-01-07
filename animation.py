"""
Add pending circle "sandclock" --> done, Percent update inplace
statusbar

"""

import asyncio
import sys
import time

class StatusBar:
    def __init__(self):
        """ Print status bar. 
        
        Args:
            max: max of range
            length: lenght of the bar in characters
        """
        self.max = 100
        self.length = 10
        print("Status: |", end="", flush=True)

    def update(self, value):
        print("#", end="", flush=True)
        if value == "stop":
            print("|")
        # check if new box is necessary -\|/_


class Spinner:
    """Differs from status bar and percent: sets own pace."""
    seq = ["|", "/", "-", "\\"]
    # seq = ["\u2665", "\u2764"]

    def __init__(self):
        self.speed = 0.18

    def run(self):
        # TODO: needs signal to stop
        print("\x1b[?25l", end="", flush=True)
        for i in range(50):
            seq = self.seq[i % len(self.seq)]
            sys.stdout.write(seq)
            sys.stdout.flush()
            time.sleep(self.speed)
            sys.stdout.write("\b" * len(seq))
        sys.stdout.write("done")
        sys.stdout.flush()
        print("\x1b[?25h", end="", flush=True)

    def stop(message):
        pass


class Percentage:
    """Needs updates."""

    def __init__(self):
        self.speed = 0.1

    def run(self):
        # TODO: needs signal to stop
        print("\x1b[?25l", end="", flush=True)
        for i in range(100):
            sys.stdout.write("{:>3}%".format(i))
            sys.stdout.flush()
            time.sleep(self.speed)
            sys.stdout.write("\b" * 4)
        sys.stdout.write("done")
        sys.stdout.flush()
        print("\x1b[?25h", end="", flush=True)

    def stop(message):
        pass

class Cat:
    cat =       ["   ^___^",
                r"°\(=^.^=)/°",
                r' (")___(")']
    altface =  "o_(=O.O=)_o"

    def __init__(self):
        self.speed = 0.1

    def run(self):
        # TODO: needs signal to stop
        print("\x1b[?25l", end="", flush=True)
        for i in range(100):
            for j, line in enumerate(self.cat):
                if j == 1 and i % 2 == 1:
                    line = self.altface
                print(" " * i + line)
                sys.stdout.flush()
            time.sleep(self.speed)
            sys.stdout.write("\x1b[K\x1b[A" * 3)
            sys.stdout.flush()
        print("\x1b[?25h", end="", flush=True)

    def stop(message):
        pass

"""
    ^___^
 °\(=^.^=)/°
  (")___(")


  _|/
<(OvO)>
 _| |_
"""


def status_demo():
    bar = StatusBar()
    for i in range(10):
        bar.update("running...")
        time.sleep(1)
    bar.update("stop")

def spinner_demo():
    s = Spinner()
    s.run()

def percent_demo():
    s = Percentage()
    s.run()



if __name__ == "__main__":
    # status_demo()
    # print("   ^___^")
    # spinner_demo()
    # percent_demo()
    cat = Cat()
    cat.run()
