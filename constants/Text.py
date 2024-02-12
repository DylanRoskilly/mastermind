class Text:
    ILL_FORMED_PLAYER = "No or ill-formed player provided"
    ILL_FORMED_CODE   = "No or ill-formed code provided"
    ILL_FORMED_GUESS  = lambda guess_num: f"Guess {guess_num}: Ill-formed guess provided"

    GUESS             = lambda guess_num, black_pegs, white_pegs: f"Guess {guess_num}: " + (" ".join((["black"] * black_pegs) + (["white"] * white_pegs)))

    LOST              = "You lost. Please try again."
    MAX_GUESSES       = lambda max_guesses: f"You can only have {max_guesses} guesses."
        
    WON               = lambda guess_num: f"You won in {guess_num} guesses. Congratulations!"
    IGNORED_LINES     = "The game was completed. Further lines were ignored."