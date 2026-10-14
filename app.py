import streamlit as st
import ollama

st.title("AI Chatbot Assistant")

SYSTEM_PROMPT = """You are a friendly assistant that helps beginners learn programming.
The user is Greek and often writes in Greeklish (Greek with Latin letters, e.g. "ti kaneis" means "how are you").
Always answer in English, with short and simple sentences,The user's name is Giorgos."""
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Ask me something...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            all_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
            response = ollama.chat(model="llama3.2", messages=all_messages)
            answer = response["message"]["content"]
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})