# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?


When I first ran the game, several bugs made it difficult or impossible to play correctly. Although the interface appeared functional, the game's logic and state management were broken.

Some of the initial bugs I encountered included incorrect hints, incorrect attempt tracking, broken newgame button, and disrepancies between the game difficulties

These bugs made the game unreliable because I couldn't trust the hints, track my remaining attempts accurately, or consistently start a new game.
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Suspected Code Loc |
|-------|-------------------|-----------------|------------------------|
| Clicked new game button | Resets attempts, comes up with a new number, and a new game is started | It resets the attempts and generates a new number, but doesn't let you play | session state attempts section

| Entered number above the secret | Hint should tell you to get lower | Tells you to go higher | unsure |


| Entered a number for first guess  | Decreases the attempts by 1 | On the first guess, attempts left doesnt decrease (remains as 7)| update score function|

| Submitted a guess (looked like the attempt wasn't recorded, had to click Submit again) | Attempts and debug info update immediately after one click | Debug expander showed a stale pre-submit set of values above the updated set | `render_status()` called twice per rerun in app.py; the expander appends instead of replacing. Fixed by rendering once, after the submit block (and before `st.stop()` on the game-over path) |

| Switched difficulty from Normal to Easy mid-game | New game with a secret in 1–20 | Secret stayed from the old range (e.g. 87), so the game was unwinnable; attempts/score carried over | `app.py` created the secret once at session start. Fixed with a `reset_game()` that also runs when the difficulty changes |

| Submitted `abc`, an empty box, or `999` on Easy | Error message, no attempt used | Attempt was consumed and junk was added to history | `attempts += 1` ran before `parse_guess`. Fixed by counting only valid guesses; `parse_guess` now also checks `low`/`high` |

| Toggled "Show hint" after a guess | Last hint stays visible | Hint vanished | Hint only rendered inside `if submit:`. Fixed by storing it in `st.session_state.last_hint` |

| Clicked New Game after a guess | Empty guess box | Old guess remained in the text box | Input key never changed. Fixed by adding a counter (`input_nonce`) to the widget key, bumped in `reset_game()` |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
ChatGPT (discussion and ideation), Claude Code (explanation and editing the actual code)


- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
One correct suggestion was to refactor the difficulty logic into logic_utils.py by creating a get_range_for_difficulty() function. The AI suggested:

def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100

This was a good fit for the project because it moved game logic out of app.py and into the logic_utils.py file as required by the assignment. I verified the suggestion by testing the different difficulty levels and checking that each one generated a secret number within the correct range.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
One AI suggestion involved changing the scoring function for an incorrect guess to:

return max(current_score - 5, 0)

I did not accept this change because it would prevent the score from becoming negative. The existing scoring system allowed negative marking, so adding a floor of zero would change the intended behavior of the game rather than simply fixing a bug.

Instead, I kept the original behavior where an incorrect guess could reduce the score below zero. This was a good reminder that an AI-generated solution can be technically reasonable while still being inconsistent with the requirements or intended behavior of a particular codebase. I verified my decision by checking the existing scoring logic and testing the resulting score behavior.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I approached debugging by reproducing each bug, identifying its likely cause by reading the code myself and flagging a location for the bug, then asking claude about the underlying logic. Then i prompted claude to implement a fix and the corresponding pytest function (both were subject to manual review by me), and then checked whether the game behaved as expected afterward.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
One manual test I ran was for the New Game functionality. After finishing a game, I clicked the New Game button and then attempted to play the newly generated game. This showed me whether the button was actually resetting the game into a playable state rather than simply resetting some of the displayed values.

I also used pytest to test the logic functions. For example, the test suite checked that different difficulty levels generated the correct number ranges, that guesses were correctly classified as wins or as too high/too low, and that the score behaved correctly for different outcomes.

- Did AI help you design or understand any tests? How?
AI helped me design pytest tests based on requirements that I provided. For example, I gave Claude the requirements for the get_range_for_difficulty() function, including the expected ranges for Easy, Normal, and Hard, and it generated pytest tests to verify those requirements. I then reviewed the generated tests myself to make sure they actually tested the intended behavior.

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit reruns a Python script from top to bottom whenever a user interacts with a widget, such as clicking a button or submitting an input. This means that ordinary Python variables can be reinitialized during each interaction.
Session state solves this problem by allowing information to persist across reruns within the same user's session.
Using st.session_state, the game can preserve important information such as the secret number, number of attempts, guess history, and most recent hint. This allows the interface to update without unintentionally resetting the game.
I also learned that Streamlit's rerun behavior affects how information should be displayed. ex, calling a rendering function multiple times can produce duplicated output rather than replacing previously displayed information. 
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
Documenting bugs with their expected and actual behavior before attempting to fix them. Creating a bug reproduction log helped me isolate individual problems instead of making several changes simultaneously without knowing which changes actually worked. It also made it easier to identify the relevant sections of code and verify whether each fix addressed the original problem.

- What is one thing you would do differently next time you work with AI on a coding task?
Next time, I would commit to git more consistently so that I would have an easier time reverting to previous versions.
I would prompt claude to commit after each fix/edit it makes

- In one or two sentences, describe how this project changed the way you think about AI generated code.
AI-generated code isn't necessarily correct simply because it runs or appears functional. AI can be a useful debugging tool, but understanding the underlying code and independently verifying its suggestions are essential to producing reliable software.