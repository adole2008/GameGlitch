from logic_utils import check_guess, update_score
from logic_utils import parse_guess, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_too_high_always_decreases_score():
    # Score must not depend on attempt parity
    for attempt in range(1, 9):
        assert update_score(50, "Too High", attempt) == 45

def test_too_high_matches_too_low():
    assert update_score(50, "Too High", 2) == update_score(50, "Too Low", 2)

def test_win_first_attempt_scores_90():
    assert update_score(0, "Win", 1) == 90

def test_win_points_have_floor_of_10():
    assert update_score(0, "Win", 20) == 10


def test_parse_guess_in_range_ok():
    assert parse_guess("20", 1, 20) == (True, 20, None)

def test_parse_guess_rejects_out_of_range():
    for raw in ("0", "21", "-5", "500"):
        ok, value, err = parse_guess(raw, 1, 20)
        assert not ok and value is None and "between 1 and 20" in err

def test_parse_guess_without_range_accepts_any_int():
    assert parse_guess("500") == (True, 500, None)

def test_parse_guess_rejects_bad_input():
    for raw in ("", "  ", "abc", "3.5", "nan", "inf", None):
        assert not parse_guess(raw, 1, 100)[0]

def test_wrong_guess_after_win_points_still_subtracts():
    assert update_score(90, "Too High", 2) == 85


# parse_guess: input handling
# A plain integer string parses to (True, int, no error)
def test_parse_valid_integer():
    assert parse_guess("42") == (True, 42, None)

# Leading/trailing spaces are ignored
def test_parse_strips_whitespace():
    assert parse_guess("  7 ") == (True, 7, None)

# '5.0' has no fractional part, so it is accepted as 5
def test_parse_whole_number_float_accepted():
    assert parse_guess("5.0") == (True, 5, None)

# Empty, whitespace-only and None input all ask the user to enter a guess
def test_parse_empty_and_none():
    assert parse_guess("") == (False, None, "Enter a guess.")
    assert parse_guess("   ") == (False, None, "Enter a guess.")
    assert parse_guess(None) == (False, None, "Enter a guess.")

# Text that is not a number is rejected with a clear message
def test_parse_non_numeric():
    assert parse_guess("abc") == (False, None, "That is not a number.")

# float() accepts these strings, so they must be rejected explicitly
def test_parse_rejects_nan_and_inf():
    for raw in ("nan", "inf", "-inf"):
        assert parse_guess(raw) == (False, None, "That is not a number.")

# FIX regression: '3.9' used to silently become 3
def test_parse_rejects_decimals_instead_of_truncating():
    assert parse_guess("3.9") == (False, None, "Enter a whole number.")


# get_range_for_difficulty
# Each difficulty maps to its documented inclusive (low, high) range
def test_range_per_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 200)

# Unrecognized difficulty falls back to the Normal range
def test_range_unknown_difficulty_defaults_to_normal():
    assert get_range_for_difficulty("Bogus") == (1, 100)
