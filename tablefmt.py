import math
import shutil
import sys

class Table:
    def __init__(self, padding=1, colsep="|", headersep="-", maxwidth=None):
        self.body = list()
        self.header = list()
        self.subheader = list()

        self.padding = padding
        self.colsep = colsep
        self.headersep = headersep
        self.maxwidth = maxwidth

        # TODO: use parameters
        self.title = ""
        self.border_left = False
        self.border_right = False
        self.border_top = False
        self.border_bottom = False

    def feed(self, body, header=list(), subheader=list()):
        self.body = body
        self.header = header
        self.subheader = subheader
        # TODO: check that number of fields is identical for each row
        # TOOO : if isinstance(body[0], list):

    def append(self, *args):
        # TODO: ccheck length
        self.body.append(list(args))

    def print(self, file=sys.stdout):
        # loop over rows and headings
        # determine widths
        # alternatively: predefine maxwidths, cut at that width?
        # distribute widths evenly
        # fixed widths for all except one

        # append all rows into table
        table = list()
        if self.header:
            table.append(self.header)
        if self.subheader:
            table.append(self.subheader)
        table.extend(self.body)

        for row_idx, _ in enumerate(table):
            for col_idx, _ in enumerate(table[row_idx]):
                # todo: convert to str
                table[row_idx][col_idx] = str(table[row_idx][col_idx])

        # todo: cut fields if some width is too long (avoid overflow)
        # TODO: check total against max width

        colwidths = self.get_colwidths(table)
        ch = " " * self.padding + self.colsep + " " * self.padding
        rowformat = ch.join(["{{:{}}}".format(width) for width in colwidths])

        # insert header line
        num_headerlines = len(table) - len(self.body)
        if self.headersep is not None and num_headerlines > 0:
            headerline = ["-" * width for width in colwidths]
            table.insert(num_headerlines, headerline)

        # todo: add outer borders

        for row in table:
            print(rowformat.format(*row), file=file)

    def from_list(self, elems, cols_first=True):
        max_length = max([len(elem) for elem in elems])
        # num_cols * max_length + (num_cols - 1) * padding = max_width
        num_cols = (max_width + padding) / (max_length + padding)
        num_rows = math.ceil(len(elems) / num_cols)

    def feed_list(self, data, cols_first=True):
        if self.maxwidth is None:
            _, self.maxwidth = self.get_terminal_size()
        for num_rows in range(1, len(data) + 1):
            num_cols =  math.ceil(len(data) / num_rows)
            body = [["" for col in range(num_cols)] for row in range(num_rows)]
            for idx, elem in enumerate(data):
                col_idx = idx // num_rows
                row_idx = idx % num_rows
                body[row_idx][col_idx] = elem
            self.body = body
            self.colsep = ""
            self.headersep = None
            self.padding = 1

            colwidths = self.get_colwidths(body)
            width = (num_cols - 1) * self.padding + sum(colwidths)
            if width <= self.maxwidth:
                return

    def single_line(self):
        """Print one single line after another, like log display."""
        pass

    def get_terminal_size(self):
        cols, rows = shutil.get_terminal_size()
        return rows, cols

    def get_colwidths(self, table):
        colwidths = [max([len(row[col_idx]) for row in table]) for col_idx in range(len(table[0]))]
        return colwidths



def main():
    data = [["Carolina", 28, 1.60],
            ["Tanja", 30, 1.68],
            ["Marco", 29, 1.83]]

    table = Table()
    table.feed(data, header=["name", "age", "height"], subheader=["", "[y]", "[m]"])
    table.print()

    data = "README.md  __pycache__/  ansiesc.py  autocomplete.py  command-loop.py  status-bar.py  table-format.py".split()
    table = Table(colsep="")
    table.feed_list(data)
    table.print()

if __name__ == "__main__":
    main()
