import itertools
import multiprocessing
from solvers.Solver import Solver


class Algorithm(Solver):
    """Base class that provides necessary attributes and methods for all algorithms.
    
    Attributes:
    num_of_colours -- number of inputted colours
    guesses, guesses_set -- stores all the current guesses
    use_multiple_processes -- whether this algorithm should use multiple processes (default: False)
    num_of_processes -- the number of processes this algorithm should use if multiple processes are enabled (default: number of cpu cores)
    guess -- the last guess made by the algorithm
    """

    def __init__(self, code: tuple[int, ...], num_of_colours: int, use_multiple_processes: bool = False) -> None:
        """Initalise the variables for an algorithm.

        Parameters:
        code -- the answer code 
        num_of_colours -- the number of available colours for this game
        use_multiple_processes - whether the algorithm should use multiple processes (default: False)
        """

        super().__init__(code)

        self.num_of_colours = num_of_colours
        
        self.guesses, self.guesses_set = [], set()

        self.use_multiple_processes = use_multiple_processes
        self.num_of_processes = multiprocessing.cpu_count()  # each process can have its own CPU core

    def generate_all_codes(self) -> list[tuple[int, ...]]:
        """Return all combinations of possible codes using self.num_of_colours and self.code_length"""

        return [code for code in itertools.product(range(self.num_of_colours), repeat=self.code_length)]
    
    def create_initial_code(self) -> tuple[int, ...]:
        """Return a tuple containing integers representing the first guess of an algorithm"""

        if self.num_of_colours == 1 or self.code_length == 1:
            return tuple([0] * self.code_length)

        half = self.code_length // 2
        return tuple(([0] * half) + ([1] * (self.code_length - half)))

    def append_guess(self):
        """Add self.guess to self.guesses_set and self.guesses"""

        self.guesses_set.add(self.guess)
        self.guesses.append(self.guess)