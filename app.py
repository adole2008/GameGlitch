import random
import streamlit as st
#FIX: Refactored logic into logic_utils.py using agent mode (update_score now imported, duplicate removed)
from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

#FIX: Refactored logic into logic_utils.py using agent mode
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

def reset_game():
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_hint = None
    # New widget key => the guess box is emptied for the new game
    st.session_state.input_nonce = st.session_state.get("input_nonce", 0) + 1


#FIX: game now resets when difficulty changes (secret used to stay from the old range)
if st.session_state.get("difficulty") != difficulty:
    st.session_state.difficulty = difficulty
    reset_game()

st.subheader("Make a guess")

info_box = st.empty()
debug_box = st.expander("Developer Debug Info")


def render_status():
    info_box.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}"
    )
    with debug_box:
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Score:", st.session_state.score)
        st.write("Difficulty:", difficulty)
        st.write("History:", st.session_state.history)


raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}_{st.session_state.input_nonce}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

#FIX: New Game now resets attempts, secret, status, score and history (agent mode)
if new_game:
    reset_game()
    st.rerun()

#FIX: render_status() now runs once per rerun (at the bottom, after submit updates state) instead of
# twice; the early call showed stale attempts in the debug expander, which appends rather than replaces.
if st.session_state.status != "playing":
    render_status()  # st.stop() below skips the bottom call
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

#FIX: Attempts counted once per submit and hints/scoring delegated to logic_utils.py using agent mode
if submit:
    #FIX: invalid or out-of-range input no longer costs an attempt or enters history
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret)

        st.session_state.last_hint = message

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

#FIX: hint is kept in session state so toggling "Show hint" (a rerun without submit) doesn't erase it
if show_hint and st.session_state.last_hint:
    st.warning(st.session_state.last_hint)

render_status()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
