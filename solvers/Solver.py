class Solver:
    """Provides properties and methods required to play the game
    
    Attributes:
    code -- answer code
    code_length -- length of the answer code
    guess_num -- current number of guesses
    """

    def __init__(self, code: tuple[int, ...]):
        """Initalise basic attributes for Solver

        Parameters:
        code -- answer code
        """

        self.code = code
        self.code_length = len(self.code)

        self.guess_num = 0

    def inc_guess_num(self) -> int: 
        """Increase the number of guesses by 1"""

        self.guess_num += 1
        return self.guess_num

    def get_pegs(self, guess: tuple[int, ...], code: tuple[int, ...]) -> tuple[int, int]:
        """Return the number of black and white pegs for a given guess and code

        Parameters:
        guess -- tuple of integers representing a guess
        code -- tuple of integers representing a code
        """

        used = [False] * self.code_length  # stores which colours in the code have been used

        freq = {}  # stores the frequency of each colour in the code
        for colour in code:
            freq[colour] = 1 if colour not in freq else freq[colour] + 1

        black_pegs = 0
        for i, colour in enumerate(guess):
            if code[i] == colour:
                black_pegs += 1
                freq[colour] -= 1
                used[i] = True

        white_pegs = 0
        for i, colour in enumerate(guess):
            # a colour can only be a white peg if its not also "used" as a black peg
            if not used[i] and colour in freq and freq[colour] > 0:
                white_pegs += 1
                freq[colour] -= 1
                used[i] = True

        return (black_pegs, white_pegs)
