#FIX: Refactored logic into logic_utils.py using agent mode
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


#FIX: Refactored into logic_utils.py using agent mode; rejects nan/inf and decimals instead of truncating
def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess, optionally checking it is within [low, high].

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    raw = raw.strip()
    if raw == "":
        return False, None, "Enter a guess."

    try:
        number = float(raw)
    except ValueError:
        return False, None, "That is not a number."

    # Reject nan/inf and decimals with a fractional part instead of
    # silently truncating them (e.g. "3.9" used to become 3).
    if number != number or number in (float("inf"), float("-inf")):
        return False, None, "That is not a number."
    if not number.is_integer():
        return False, None, "Enter a whole number."

    value = int(number)
    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Enter a number between {low} and {high}."

    return True, value, None


#FIX: Refactored into logic_utils.py using agent mode; hints now correct (high -> LOWER, low -> HIGHER)
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


#FIX: Refactored into logic_utils.py using agent mode; Too High always -5 (no attempt-parity quirk)
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number (1-based)."""
    if outcome == "Win":
        points = max(100 - 10 * attempt_number, 10)
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        #AI fix rejected: floor the score at 0 (would make negative marking meaningless)
        return current_score - 5

    return current_score
