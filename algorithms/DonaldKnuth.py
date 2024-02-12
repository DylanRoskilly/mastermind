import math
import multiprocessing
from algorithms.Algorithm import Algorithm


class DonaldKnuthAlgorithm(Algorithm):
    """Guesses the code using Donald Knuth's Five Guess algorithm.
    
    Attributes:
    all_codes -- a list of all possible code combinations
    num_of_codes -- the total number of all possible code combinations
    remaining_codes -- a set of the codes which could possibly be the answer code
    part -- number of codes each process should search, if using multiple processes
    pegs -- a tuple storing the (black_pegs, white_pegs) of the last guess
    """

    def __init__(self, code: tuple[int, ...], num_of_colours: int, use_multiple_processes: bool = False) -> None:
        """Initalise the variables for Donald Knuth's algorithm.

        Parameters:
        code -- the answer code 
        num_of_colours -- the number of available colours for this game
        use_multiple_processes - whether the algorithm should use multiple processes (default: False)
        """

        super().__init__(code, num_of_colours, use_multiple_processes)

        self.all_codes = self.generate_all_codes()
        self.remaining_codes = set(self.all_codes)
        self.num_of_codes = len(self.all_codes)
        
        if self.use_multiple_processes: 
            # calculate how many codes each process will handle
            self.part = math.ceil(self.num_of_codes / self.num_of_processes) 

    def min_max_score(self, start: int, end: int, min_scores: list[tuple[int, int]]) -> None:
        """Performs the MinMax of the Donald Knuth's Five Guess algorithm on a specified section of self.all_codes
        
        Parameters:
        start -- the index at the beginning of this function's allocated section
        end -- the index at the end of this function's allocated section
        min_scores -- an output list to store the min_score and the codes with this min_score
        """

        min_score = float("inf")
        codes = []
        
        for i in range(start, end):
            code = self.all_codes[i]

            if code in self.guesses_set:  # don't want to make the same guess twice
                continue

            # stores all possible black, white peg combinations against the number of 
            # times this combination occurs (called "score") e.g. scores[(0, 3)] = 5
            scores = {}  
            for guess in self.remaining_codes:
                pegs = self.get_pegs(guess, code)
                scores[pegs] = 1 if pegs not in scores else scores[pegs] + 1

            # gets the peg combination (key) with the highest score (value)
            max_score = max(scores, key=scores.get, default=None)  
            score = scores[max_score]

            # update codes to contain the codes with the lowest score
            if score < min_score:
                min_score = score
                codes = [code]
            elif min_score == score:
                codes.append(code)

        min_scores.append((min_score, codes))

    def get_next_guess(self) -> tuple[int, int]:
        """Find the next guess using Donald Knuth's Five Guess algorithm."""

        if self.guess_num == 1:
            self.guess = self.create_initial_code()
        else:
            # filter remaining codes to include only codes which would give the same pegs if they were the code
            self.remaining_codes = {code for code in self.remaining_codes if self.get_pegs(self.guess, code) == self.pegs}

            codes = []
            if not self.use_multiple_processes:
                min_scores = []
                self.min_max_score(0, self.num_of_codes, min_scores)
                _, codes = min_scores[0]
            else:
                manager = multiprocessing.Manager()
                min_scores = manager.list()  # create a mutex list which can safely be shared between concurrent processes

                processes = []
                remaining = self.num_of_codes
                while remaining > 0:  # create processes until all processes cover every index in self.remaining_codes
                    args = (max(0, remaining-self.part), remaining, min_scores)
                    remaining -= self.part

                    process = multiprocessing.Process(target=self.min_max_score, args=args) 
                    processes.append(process)
                    process.start()

                for process in processes:
                    process.join()

                # its possible for multiple processes to find the same minimum score
                # so merge all codes with this minimum score into a single list
                min_score, _ = min(min_scores)
                for score, c in min_scores:
                    if score == min_score:
                        codes += c
            
            # choose the guess as the code which is in remaining codes
            self.guess = codes[0]
            i = 1
            while self.guess not in self.remaining_codes and i < len(codes):
                self.guess = codes[i]
                i += 1

        self.append_guess()

        self.pegs = (black_pegs, white_pegs) = self.get_pegs(self.guess, self.code)

        return (black_pegs, white_pegs)
