from algorithms.DonaldKnuth import DonaldKnuthAlgorithm
from algorithms.Swaszek import SwaszekAlgorithm


class ComputerSolver:
    """Represents the computer player
    
    Attributes:
    algorithm -- the algorithm which should be used to find this code
    """

    def __init__(self, code: tuple[int, ...], num_of_colours: int) -> None:
        """Intialise the algorithm based on the number_of_colours and code length
        Donald Knuth's algorithm takes more time but less guesses. 
        Swaszek's algorithm takes less time but more guesses. 
        
        Parameters: 
        code -- the answer code
        num_of_colours -- the number of inputted colours
        """

        num_of_codes = pow(num_of_colours, len(code))
        
        # I benchmarked with a variety of code lengths and number of colours and these ranges
        # provided the best number of guesses vs time taken ratio
        if num_of_codes <= 2187:
            self.algorithm = DonaldKnuthAlgorithm(code, num_of_colours)
        elif num_of_codes <= 15625:
            self.algorithm = DonaldKnuthAlgorithm(code, num_of_colours, True)
        elif num_of_codes <= 390625:
            self.algorithm = SwaszekAlgorithm(code, num_of_colours)
        else:
            self.algorithm = SwaszekAlgorithm(code, num_of_colours, True)

    def get_next_guess(self) -> tuple[int, int]:
        """Get the next guess from the chosen algorithm and return this guess' (black_pegs, white_pegs)"""
        
        return self.algorithm.get_next_guess()

    def inc_guess_num(self) -> int:
        """Increase the number of guesses"""
        
        return self.algorithm.inc_guess_num()

    def get_guesses(self) -> list[tuple[int, ...]]:
        """Return a list of the number of guesses that the algorithm has currently made"""

        return self.algorithm.guesses