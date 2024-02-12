class LineStream:
    """Stores a file and allows you to access one line after another, in the order they appear in the file.
    All whitespace in the line is removed and split by spaces. 

    Attributes:
    file -- the file to get lines from
    lines -- all the lines in the file
    i -- index of the current line
    """

    def __init__(self, file) -> None:
        """Store the file as an attribute"""
        
        self.file = file
        self.lines = self.file.readlines()
        self.i = 0

    def is_eof(self) -> bool:
        """Return if there are any more lines to read"""

        return self.i == len(self.lines)

    def get_next_line(self) -> list[str]:
        """Return the cleaned version of the next line in the file.
        The "cleaned version" of the line contains no \n nor spaces. The line is split by spaces.
        """

        line = self.lines[self.i]
        self.i += 1

        return line.strip().split(" ")