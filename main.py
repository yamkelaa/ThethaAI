import streamlit as st
from chatbot import XhosaChatbot
import time

st.set_page_config(
    page_title="Xhosa Chatbot",
    page_icon="🗣️",
    layout="wide"
)

if 'chatbot' not in st.session_state:
    st.session_state.chatbot = XhosaChatbot(n=3, mode='word')
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'n_value' not in st.session_state:
    st.session_state.n_value = 3
if 'mode' not in st.session_state:
    st.session_state.mode = 'word'

st.title("🗣️ Xhosa N-gram Chatbot")
st.markdown("Chat with an autoregressive Xhosa language model using n-grams")

with st.sidebar:
    st.header("Configuration")
    
    n_value = st.slider("N-gram Order", min_value=2, max_value=5, value=3)
    
    mode = st.radio("Generation Mode", ['word', 'character'])
    
    if st.button("Apply Settings"):
        st.session_state.chatbot = XhosaChatbot(n=n_value, mode=mode)
        st.session_state.n_value = n_value
        st.session_state.mode = mode
        st.session_state.conversation = []
        st.success("Settings applied!")
    
    st.markdown("---")
    st.markdown("### Sample Generation")
    sample_prompt = st.text_input("Enter prompt for sample generation:")
    if st.button("Generate Sample"):
        sample = st.session_state.chatbot.generate_sample(sample_prompt, length=20)
        st.text_area("Generated Sample:", sample, height=100)

user_input = st.chat_input("Type your message in Xhosa...")

if user_input:
    st.session_state.conversation.append(("You", user_input))
    
    with st.spinner("Thinking..."):
        time.sleep(0.5) 
        response = st.session_state.chatbot.respond(user_input)
    
    st.session_state.conversation.append(("Bot", response))
    st.rerun()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Chat")
    
    for i, (speaker, message) in enumerate(st.session_state.conversation):
        if speaker == "You":
            st.chat_message("user").write(message)
        else:
            st.chat_message("assistant").write(message)

with col2:
    st.subheader("Model Info")
    st.info(f"""
    **Current Settings:**
    - N-gram order: {st.session_state.n_value}
    - Generation mode: {st.session_state.mode}
    - Vocabulary size: {len(st.session_state.chatbot.model.vocab)}
    """)
    
    st.markdown("---")
    st.subheader("Try These Phrases:")
    sample_phrases = [
        "Molo",
        "Unjani",
        "Igama lakho ngubani",
        "Uvela phi",
        "Uyasebenza"
    ]
    
    for phrase in sample_phrases:
        if st.button(phrase, key=phrase):
            st.session_state.conversation.append(("You", phrase))
            response = st.session_state.chatbot.respond(phrase)
            st.session_state.conversation.append(("Bot", response))
            st.rerun()

if st.sidebar.button("Clear Conversation"):
    st.session_state.conversation = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using n-gram models")