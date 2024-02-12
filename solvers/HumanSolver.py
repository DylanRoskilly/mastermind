from solvers.Solver import Solver


class HumanSolver(Solver):
    """Represents a human player"""

    def __init__(self, code: tuple[int, ...]) -> None:
        """Initalise the super class"""

        super().__init__(code)

    def get_next_guess(self, guess: tuple[int, ...]) -> tuple[int, int]:
        """Return the (black_pegs, white_pegs) for the inputted guess
        
        Parameters:
        guess - the code to compare to the correct code
        """ 

        return self.get_pegs(guess, self.code)
