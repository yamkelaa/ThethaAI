import streamlit as st
import pickle
from pathlib import Path
import random

MODEL_PATH = Path("src/model/ngram_model.pkl")

# Load trained model
with open(MODEL_PATH, "rb") as f:
    data = pickle.load(f)

input_to_response = data["input_to_response"]
ngram_model = data["ngram_model"]

st.set_page_config(
    page_title="🗣️ ThethaAI – isiXhosa Conversational Demo",
    page_icon="🗣️",
    layout="centered"
)

st.title("🗣️ ThethaAI – isiXhosa Conversational Demo")
st.write("Enter multiple isiXhosa sentences or phrases (one per line) and get responses.")

user_input = st.text_area("👉 Enter text:", height=150)
num_words = st.slider("Length of generated response (words)", min_value=5, max_value=50, value=20)

def generate_text(model, n=2, max_words=20):
    start = ("~",) * (n - 1)
    result = list(start)
    for _ in range(max_words):
        key = tuple(result[-(n - 1):])
        possible = model.get(key, ["~"])
        next_word = random.choice(possible)
        if next_word == "~":
            break
        result.append(next_word)
    return " ".join(result[(n - 1):])

if st.button("Generate Responses"):
    inputs = [line.strip() for line in user_input.split("\n") if line.strip()]
    if not inputs:
        st.warning("Please enter at least one line of text.")
    else:
        st.subheader("🤖 ThethaAI Responses:")
        for i, text in enumerate(inputs, 1):
            key = text.lower()
            if key in input_to_response:
                response = input_to_response[key]
            else:
                response = generate_text(ngram_model, n=2, max_words=num_words)
            st.markdown(f"**Input {i}:** {text}")
            st.markdown(f"**Response {i}:** {response}")
            st.write("---")
