import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("questions.csv", names=["Q", "A", "B", "C", "D", "Link"])

st.title("Trivia Quest 🧠")

if 'count' not in st.session_state:
    st.session_state.count = 0

# Check if quiz is over
if st.session_state.count >= len(df):
    st.balloons()
    st.success("Quiz Complete!")
    if st.button("Restart Quiz"):
        st.session_state.count = 0
        st.rerun()
    st.stop()

row = df.iloc[st.session_state.count]

# CLEANING: This handles spaces AND quotes perfectly
raw_options = [str(row.A), str(row.B), str(row.C), str(row.D)]
clean_options = [opt.strip().strip('"') for opt in raw_options]

st.write(f"### Question {st.session_state.count + 1}")
st.subheader(row.Q)

# UI for selection
selection = st.radio(
    "Select an option:",
    clean_options,
    index=None,
    key=f"radio_{st.session_state.count}"
)

# Create two columns for the buttons
col1, col2 = st.columns([1, 4])

with col1:
    if st.button("Skip ⏭️"):
        st.session_state.count += 1
        st.rerun()

# Logic when an answer is chosen
if selection:
    # Find the original raw string to check for the " " 
    selected_index = clean_options.index(selection)
    was_correct = '"' in raw_options[selected_index]
    
    if was_correct:
        st.success("Correct! 🎉")
    else:
        # Find which one was correct to show the user
        correct_text = next(opt.strip().strip('"') for opt in raw_options if '"' in opt)
        st.error(f"Wrong. The correct answer was: {correct_text}")
    
    if st.button("Next Question →"):
        st.session_state.count += 1
        st.rerun()
