from enum import Enum


class ExitCodes(Enum):
    SUCCESS           = 0  # The programme ran successfully
    ARGS_ERROR        = 1  # Not enough programme arguments provided
    INPUT_FILE_ERROR  = 2  # There was an issue with the input file
    OUTPUT_FILE_ERROR = 3  # There was an issue with the output file
    CODE_ERROR        = 4  # No or ill-formed code provided
    PLAYER_ERROR      = 5  # No or ill-formed player provided


class Player(Enum):
    HUMAN    = 0 
    COMPUTER = 1 