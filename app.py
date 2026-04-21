import streamlit as st
import pandas as pd

# Load your data
df = pd.read_csv("questions.csv", names=["Q", "A", "B", "C", "D", "Link"])

st.title("Trivia Quest")

# Track which question we are on
if 'count' not in st.session_state:
    st.session_state.count = 0

# Show the question
row = df.iloc[st.session_state.count]
st.write(f"### {row.Q}")

# User picks an answer
choice = st.radio("Select your answer:", [row.A, row.B, row.C, row.D])

if st.button("Submit"):
    if '"' in choice: # Your CSV uses quotes for correct answers
        st.success("Correct!")
    else:
        st.error("Wrong!")

if st.button("Next Question"):
    st.session_state.count += 1
    st.rerun()
