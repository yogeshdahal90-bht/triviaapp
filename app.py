import streamlit as st
import pandas as pd

# Load data - assuming no header row in CSV
df = pd.read_csv("questions.csv", names=["Q", "A", "B", "C", "D", "Link"])

st.title("Trivia Quest 🧠")

# Initialize session state
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False

# Stop if we run out of questions
if st.session_state.count >= len(df):
    st.success("You've finished the quiz!")
    if st.button("Restart"):
        st.session_state.count = 0
        st.rerun()
    st.stop()

row = df.iloc[st.session_state.count]

# Clean the options (remove quotes for display)
raw_options = [row.A, row.B, row.C, row.D]
clean_options = [opt.strip('"') for opt in raw_options]

st.write(f"### Question {st.session_state.count + 1}")
st.write(row.Q)

# The Radio button - we add an empty index so nothing is pre-selected
selection = st.radio(
    "Choose your answer:",
    clean_options,
    index=None,
    key=f"q_{st.session_state.count}" # Unique key per question
)

# Logic: As soon as they select something
if selection:
    # Find if the raw version of their selection had quotes
    actual_selection_raw = raw_options[clean_options.index(selection)]
    
    if '"' in actual_selection_raw:
        st.success("Correct! 🎉")
    else:
        # Find the correct one to show them
        correct_answer = next(opt.strip('"') for opt in raw_options if '"' in opt)
        st.error(f"Not quite. The correct answer was: {correct_answer}")

    # Show "Next" button immediately after selection
    if st.button("Next Question →"):
        st.session_state.count += 1
        st.session_state.answered = False
        st.rerun()
