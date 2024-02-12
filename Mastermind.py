import sys
from typing import Union
from constants.Text import Text
from constants.enums import ExitCodes, Player
from utils.LineStream import LineStream
from utils.Validator import Validator
from solvers.ComputerSolver import ComputerSolver
from solvers.HumanSolver import HumanSolver


class Mastermind:
    def __init__(self) -> None:
        self.validator = Validator()

        self.process_args()

        self.read_input_file()
        self.open_output_file()

        self.get_code()
        self.get_player()

        # This would be better using match ... case but its not available in required the Python version
        if self.player == Player.HUMAN:
            self.play_human_game()
        elif self.player == Player.COMPUTER:
            self.play_computer_game()

        self.exit(ExitCodes.SUCCESS)

    def process_args(self) -> None:
        """Declare the properties of this object from the command line arguments.

        Format of arguments:
        python Mastermind.py InputFile OutputFile [CodeLength] [MaximumGuesses] [AvailableColour]*
        """

        num_of_args = len(sys.argv)
        if num_of_args < 3:
            self.exit(ExitCodes.ARGS_ERROR)

        self.input_file_name = sys.argv[1]
        self.output_file_name = sys.argv[2]

        self.code_length = int(sys.argv[3]) if num_of_args > 3 and self.validator.is_positive_integer(sys.argv[3]) else 5
        self.max_guesses = int(sys.argv[4]) if num_of_args > 4 and self.validator.is_positive_integer(sys.argv[4]) else 12

        if num_of_args > 6:
            input_colours = sys.argv[5:num_of_args]

            # avoid duplicate colours
            self.colours = []
            self.colours_map = {}
            i = 0
            for colour in input_colours:
                if colour not in self.colours_map:
                    self.colours.append(colour)
                    self.colours_map[colour] = i  # store colour against its index in self.colours
                    i += 1
        else:
            self.colours = ["red", "blue", "yellow", "green", "orange"]
            self.colours_map = {colour: i for i, colour in enumerate(self.colours)}

        self.num_of_colours = len(self.colours)

    def read_input_file(self) -> None:
        """Create a LineStream for the input file so the lines can be read later.
        Exit if the file cannot be opened.
        """

        try:
            self.lines = LineStream(open(self.input_file_name, "r"))
        except:
            self.exit(ExitCodes.INPUT_FILE_ERROR)

    def open_output_file(self) -> None:
        """Open the output file and assign it to the output_file attribute.
        Exit if the file cannot be opened.
        """

        try:
            self.output_file = open(self.output_file_name, "w")
        except:
            self.exit(ExitCodes.OUTPUT_FILE_ERROR)

    def format_code(self, code: list[str]) -> Union[tuple[int, ...], None]:
        """Convert a string of colour names into a tuple of integers, if the colours are valid.
        Otherwise, return None.
        """

        if len(code) != self.code_length:
            return None

        formatted_code = []
        
        for colour in code:
            if colour not in self.colours_map:  # determine if the colour exists
                return None
            formatted_code.append(self.colours_map[colour])

        return tuple(formatted_code)

    def code_to_text(self, code: tuple[int, ...]) -> str:
        """Convert the code (as a tuple of integers) into a string of colour names."""

        return " ".join(self.colours[colour_index] for colour_index in code)

    def get_code(self) -> None:
        """Set self.code as the formatted inputted code, if its valid.
        Otherwise, return exit code.
        """
        
        if self.lines.is_eof():
            self.exit(ExitCodes.CODE_ERROR)

        line_one = self.lines.get_next_line()
        if len(line_one) != (self.code_length + 1) or line_one[0] != "code":
            self.exit(ExitCodes.CODE_ERROR)

        self.code = self.format_code(line_one[1:])
        if self.code is None:
            self.exit(ExitCodes.CODE_ERROR)

    def get_player(self) -> None:
        """Set self.player as one of the Player enum values for the inputted player, if its valid.
        Otherwise, return exit code.
        """
        
        if self.lines.is_eof():
            self.exit(ExitCodes.PLAYER_ERROR)

        line_two = self.lines.get_next_line()
        if len(line_two) != 2 or line_two[0] != "player":
            self.exit(ExitCodes.PLAYER_ERROR)

        player = line_two[1]
        if player != "human" and player != "computer":
            self.exit(ExitCodes.PLAYER_ERROR)

        self.player = Player.HUMAN if player == "human" else Player.COMPUTER

    def play_human_game(self) -> None:
        solver = HumanSolver(self.code)

        lines = []

        while True:
            if self.lines.is_eof():  # EOF reached
                lines.append(Text.LOST)
                break
            
            guess_num = solver.inc_guess_num()
            if guess_num > self.max_guesses:
                lines.append(Text.LOST)
                lines.append(Text.MAX_GUESSES(self.max_guesses))
                break

            guess = self.format_code(self.lines.get_next_line())

            if guess is None:
                lines.append(Text.ILL_FORMED_GUESS(guess_num))
            else:
                (black_pegs, white_pegs) = solver.get_next_guess(guess)

                lines.append(Text.GUESS(guess_num, black_pegs, white_pegs))

                if black_pegs == self.code_length:
                    lines.append(Text.WON(guess_num))
                    if not self.lines.is_eof():  # determine if there were more guesses
                        lines.append(Text.IGNORED_LINES)
                    break

        self.write_lines(lines, self.output_file)

    def play_computer_game(self) -> None:
        """Tries to guess the inputted code using only feedback from previous guesses.

        Guesses are added to the computerGame.txt file.
        Feedback from guesses are added to the output file.
        """

        solver = ComputerSolver(self.code, self.num_of_colours)

        lines = []

        while True:
            guess_num = solver.inc_guess_num()
            if guess_num > self.max_guesses:
                lines.append(Text.LOST)
                break

            (black_pegs, white_pegs) = solver.get_next_guess()

            lines.append(Text.GUESS(guess_num, black_pegs, white_pegs))

            if black_pegs == self.code_length:
                lines.append(Text.WON(guess_num))
                break

        self.write_lines(lines, self.output_file)

        lines = [
            "code " + self.code_to_text(self.code),
            "player human"
        ]
        for guess in solver.get_guesses():
            lines.append(self.code_to_text(guess))

        try:
            file = open("computerGame.txt", "w")
            self.write_lines(lines, file)
            file.close()
        except:
            self.exit(ExitCodes.OUTPUT_FILE_ERROR)

    def write_lines(self, lines: list[str], file: 'File') -> None:
        """Write a list of strings to a file, creates a new line after every string.

        Parameters:
        lines -- the list of strings to write, each string should NOT end with \n
        file -- the file to write to
        """

        try:
            file.writelines("\n".join(lines) + "\n")
        except:
            self.exit(ExitCodes.OUTPUT_FILE_ERROR)

    def exit(self, error: ExitCodes) -> None:
        """Write the specified exit code to the output file (if required) and return this exit code.

        Parameters:
        error -- the enum value of the exit code
        """

        if hasattr(self, "output_file"):  # determines if the output file has been opened
            if error == ExitCodes.CODE_ERROR:
                self.write_lines([Text.ILL_FORMED_CODE], self.output_file)
            elif error == ExitCodes.PLAYER_ERROR:
                self.write_lines([Text.ILL_FORMED_PLAYER], self.output_file)

            self.output_file.close()

        sys.exit(error.value)


if __name__ == '__main__':
    Mastermind()
