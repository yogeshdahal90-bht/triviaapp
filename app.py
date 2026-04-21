import streamlit as st
import pandas as pd
import random

# Load data
df = pd.read_csv("questions.csv", names=["Q", "A", "B", "C", "D", "Link"])

st.title("Trivia Quest 🧠")

# 1. Selection Logic: Choose 10 random questions once per session
if 'quiz_data' not in st.session_state:
    # Shuffle and pick 10
    st.session_state.quiz_data = df.sample(n=10).reset_index(drop=True)
    st.session_state.count = 0
    st.session_state.score = 0

# Use the 10 random questions instead of the full list
current_quiz = st.session_state.quiz_data

# Final Results Screen
if st.session_state.count >= len(current_quiz):
    st.balloons()
    st.header("Assessment Complete! 🏆")
    st.metric(label="Final Score", value=f"{st.session_state.score} pts")
    
    accuracy = int((st.session_state.score / (len(current_quiz) * 100)) * 100)
    st.write(f"Your accuracy for this round: **{accuracy}%**")

    if st.button("Play Again (New Questions)"):
        # Clear session state to trigger a new random selection
        del st.session_state.quiz_data
        st.rerun()
    st.stop()

# Progress Sidebar
st.sidebar.write(f"### Score: {st.session_state.score}")
st.sidebar.progress((st.session_state.count) / len(current_quiz))
st.sidebar.write(f"Question {st.session_state.count + 1} of {len(current_quiz)}")

row = current_quiz.iloc[st.session_state.count]

# CLEANING
raw_options = [str(row.A), str(row.B), str(row.C), str(row.D)]
clean_options = [opt.strip().strip('"') for opt in raw_options]

st.write(f"### Question {st.session_state.count + 1}")
st.subheader(row.Q)

selection = st.radio(
    "Select an option:",
    clean_options,
    index=None,
    key=f"radio_{st.session_state.count}"
)

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Skip ⏭️"):
        st.session_state.count += 1
        st.rerun()

# Scoring Logic
if selection:
    selected_index = clean_options.index(selection)
    was_correct = '"' in raw_options[selected_index]
    
    # Ensure point is only added once per question
    if 'last_answered' not in st.session_state or st.session_state.last_answered != st.session_state.count:
        if was_correct:
            st.session_state.score += 100
            st.success("Correct! +100 Points 🎉")
        else:
            correct_text = next(opt.strip().strip('"') for opt in raw_options if '"' in opt)
            st.error(f"Wrong. The correct answer was: {correct_text}")
        
        st.session_state.last_answered = st.session_state.count
    
    if st.button("Next Question →"):
        st.session_state.count += 1
        st.rerun()
