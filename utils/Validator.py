class Validator:
    """Provides methods to valid inputs.

    Attributes:
    integers -- set of all integers [0, 9]
    """

    def __init__(self):
        """Initalise a set of integers."""

        self.integers = set(str(i) for i in range(10))
    
    def is_positive_integer(self, x: str) -> bool:
        """Return whether x is an integer greater than 0. Doesn't allow leading zeros.
        
        Parameters:
        x -- the string containing possible integers
        """

        return len(x) > 0 and x.lstrip("0") == x and all(digit in self.integers for digit in x)
