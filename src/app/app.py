import streamlit as st
import pickle
from pathlib import Path
from src.model.ngram import generate_text

# Load trained model
MODEL_PATH = Path("data/processed/ngram_model.pkl")
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

st.title("🗣️ ThethaAI – isiXhosa Conversational Demo")

st.write("You can enter multiple isiXhosa sentences or phrases (one per line).")
user_input = st.text_area("👉 Enter text:", height=150)

num_chars = st.slider("Length of generated response (characters)", min_value=30, max_value=200, value=80)

if st.button("Generate Responses"):
    # Split input into lines
    inputs = [line.strip() for line in user_input.split("\n") if line.strip()]

    if not inputs:
        st.warning("Please enter at least one line of text.")
    else:
        st.subheader("🤖 ThethaAI Responses:")
        for i, text in enumerate(inputs, 1):
            response = generate_text(model, length=num_chars, n=3)
            st.markdown(f"**Input {i}:** {text}")
            st.markdown(f"**Response {i}:** {response}")
            st.write("---")
