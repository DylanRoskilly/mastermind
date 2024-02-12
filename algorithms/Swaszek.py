import math
import multiprocessing
from algorithms.Algorithm import Algorithm


class SwaszekAlgorithm(Algorithm):
    """Guesses the code using Swaszek's (1999-2000) algorithm.
    
    Attributes:
    remaining_codes -- a set of the codes which could possibly be the answer code
    num_of_codes -- number of remaining codes
    pegs -- a tuple storing the (black_pegs, white_pegs) of the last guess
    """

    def __init__(self, code: tuple[int, ...], num_of_colours: int, use_multiple_processes: bool = False) -> None:
        """Initalise the variables for Swaszek's algorithm.

        Parameters:
        code -- the answer code 
        num_of_colours -- the number of available colours for this game
        use_multiple_processes - whether the algorithm should use multiple processes (default: False)
        """

        super().__init__(code, num_of_colours, use_multiple_processes)

        self.remaining_codes = self.generate_all_codes()
        self.num_of_codes = len(self.remaining_codes)

    def filter(self, start: int, end: int, remaining_codes: list[tuple[int, ...]]) -> None:
        """Remove all codes from self.remaining_codes, which would not give the 
        same answer if they were the code, within the given index range [start, end)
        
        Parameters:
        start -- the index at which this process should start filtering
        end -- the index at which this process should stop
        remaining_codes -- output list containing all filtered codes
        """

        # It is faster to create an intermediate list and update remaining_codes at the 
        # end since remaining_codes has a mutex guard and I do not want each process to wait 
        # for write access each time they want to append a code
        codes = []

        for i in range(start, end):
            if self.get_pegs(self.guess, self.remaining_codes[i]) == self.pegs:
                codes.append(self.remaining_codes[i])

        remaining_codes += codes
        
    def get_next_guess(self) -> tuple[int, int]:
        if self.guess_num == 1:
            self.guess = self.create_initial_code()
        else:
            part = math.ceil(self.num_of_codes / self.num_of_processes)  # calculate how many codes each process will filter
            
            # I do not use multiple processes if use_multiple_processes is true and part is 
            # less than 150 because it takes more time to initalise every process compared to 
            # just searching through (150 * num_of_processes) codes on a single process
            if not self.use_multiple_processes or (self.use_multiple_processes and part < 150):
                self.remaining_codes = [code for code in self.remaining_codes if self.get_pegs(self.guess, code) == self.pegs]
            else:
                manager = multiprocessing.Manager()
                remaining_codes = manager.list()  # create a mutex list which can safely be shared between concurrent processes

                processes = []
                remaining = self.num_of_codes  # number of remaining codes which have not been allocated a process
                while remaining > 0:
                    args = (max(0, remaining-part), remaining, remaining_codes)
                    remaining -= part

                    process = multiprocessing.Process(target=self.filter, args=args) 
                    processes.append(process)
                    process.start()

                for process in processes:  # wait for all processes to terminate
                    process.join() 

                self.remaining_codes = remaining_codes  # update self.remaining_codes to the results from the processes
                self.num_of_codes = len(self.remaining_codes)
            
            # find the first remaining code which has not been used as a guess before
            self.guess = self.remaining_codes[0]
            i = 1
            while self.guess in self.guesses_set and i < len(self.guesses): 
                self.guess = self.remaining_codes[i]
                i += 1

        self.append_guess()       

        self.pegs = (black_pegs, white_pegs) = self.get_pegs(self.guess, self.code)

        return (black_pegs, white_pegs)
