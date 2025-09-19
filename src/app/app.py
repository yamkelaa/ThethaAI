import streamlit as st
import pickle
from pathlib import Path
from src.model.ngram import generate_text

st.set_page_config(
    page_title="🗣️ ThethaAI – isiXhosa Word N-gram Demo",
    page_icon="🗣️",
    layout="centered"
)

MODEL_PATH = Path("src/model/ngram_model.pkl")
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

st.title("🗣️ ThethaAI – isiXhosa Word N-gram Demo")
st.write("This model generates isiXhosa-like text using word-level n-grams.")

num_words = st.slider("Length of generated response (words)", min_value=5, max_value=50, value=15)

if st.button("Generate Text"):
    response = generate_text(model, n=3, max_words=num_words)
    st.subheader("🤖 Generated Text:")
    st.markdown(response)
