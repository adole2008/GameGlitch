# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

Purpose: The game is a Streamlit-based number guessing game where the player attempts to guess a randomly generated secret number within a limited number of attempts. The player can choose between different difficulty levels, receive higher/lower hints, and track their attempts, guesses, and score. The project was designed to practice debugging a Streamlit application, managing session state, separating game logic from the UI, and writing automated tests.

Bugs Found:
I found several bugs involving game state, game logic, input validation, scoring, and the UI:
1. New Game was not playable: Clicking New Game reset the number of attempts and generated a new secret number, but the resulting game could not be played correctly.
2. Hints were backwards: Entering a guess above the secret number caused the game to tell the player to guess higher instead of lower.
3. First guess did not decrease attempts: The first submitted guess did not correctly reduce the number of remaining attempts.
4. Debug information was duplicated/stale: The debug information was rendered more than once during a rerun, causing an old set of values to appear above the updated values.
5. Changing difficulty did not reset the game: Switching difficulty during a game could leave the player with a secret number from the previous difficulty range, making the game potentially impossible to win.
6. Invalid guesses consumed attempts: Invalid inputs such as letters, empty input, or numbers outside the selected range were counted as attempts and added to the guess history.
7. Hints disappeared: Toggling the Show Hint option after submitting a guess caused the previous hint to disappear.
8. Previous guess remained after New Game: Starting a new game did not clear the old guess from the input box.

Quick Rundown of Fixes Applied:
I fixed the bugs by:
- Refactoring the game logic into logic_utils.py.
- Using Streamlit session state to preserve the secret number and other game information across reruns.
- Correcting the higher/lower comparison logic.
- Fixing the attempt counter so that valid guesses consume an attempt exactly once.
- Moving the status rendering so that the debug information is updated correctly rather than rendered twice.
- Adding a reset_game() function that resets the secret number, attempts, score, guess history, and other game state when starting a new game or changing difficulty.
- Updating input validation so invalid guesses do not consume an attempt or get added to the guess history.
- Storing the most recent hint in st.session_state.last_hint so that it persists across reruns.
- Adding an input_nonce to the input widget key so that the guess box is cleared when a new game begins.
- Adding and running pytest tests to verify the behavior of the refactored game logic.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Select a difficulty level. The game generates a secret number within the appropriate range for the selected difficulty.
2. Enter a guess and submit it. The game checks whether the guess is valid and, if it is, records the guess and decreases the number of remaining attempts.
3. Use the hint to adjust the next guess. If the guess is too low, the game displays a "Higher" hint; if the guess is too high, it displays a "Lower" hint.
4. Continue guessing until the secret number is found or the attempts run out. The player's score and guess history update as the game progresses.
5. Start a new game. Clicking New Game resets the previous game's state, generates a new secret number, clears the previous guess, and allows the player to immediately begin another game.
6. Change difficulty when needed. Changing the difficulty starts a fresh game using the correct number range for the newly selected difficulty.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->
![alt text](image.png)

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
python -m pytest
================================================================== test session starts ===================================================================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: [removed]
collected 21 items                                                                                                                                       

tests/test_game_logic.py .....................                                                                                                     [100%]

=================================================================== 21 passed in 0.04s ===================================================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
