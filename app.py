import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("questions.csv", names=["Q", "A", "B", "C", "D", "Link"])

st.title("Trivia Quest 🧠")

# Initialize points and counter
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'score' not in st.session_state:
    st.session_state.score = 0

# Final Results Screen
if st.session_state.count >= len(df):
    st.balloons()
    st.header("Assessment Complete! 🏆")
    
    # Big score display
    st.metric(label="Final Score", value=f"{st.session_state.score} pts")
    
    accuracy = int((st.session_state.score / (len(df) * 100)) * 100)
    st.write(f"Your accuracy: **{accuracy}%**")

    if st.button("Restart Session"):
        st.session_state.count = 0
        st.session_state.score = 0
        st.rerun()
    st.stop()

# Progress and Current Score
st.sidebar.write(f"### Session Score: {st.session_state.score}")
st.sidebar.progress((st.session_state.count) / len(df))

row = df.iloc[st.session_state.count]

# CLEANING
raw_options = [str(row.A), str(row.B), str(row.C), str(row.D)]
clean_options = [opt.strip().strip('"') for opt in raw_options]

st.write(f"### Question {st.session_state.count + 1} / {len(df)}")
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
    
    if 'last_answered' not in st.session_state or st.session_state.last_answered != st.session_state.count:
        if was_correct:
            st.session_state.score += 100
            st.success("Correct! +100 Points 🎉")
        else:
            correct_text = next(opt.strip().strip('"') for opt in raw_options if '"' in opt)
            st.error(f"Wrong. The correct answer was: {correct_text}")
        
        # Mark this question as "accounted for" so they can't spam points
        st.session_state.last_answered = st.session_state.count
    
    if st.button("Next Question →"):
        st.session_state.count += 1
        st.rerun()
