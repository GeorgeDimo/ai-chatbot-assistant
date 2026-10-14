import streamlit as st
import ollama
from ddgs import DDGS


st.title("AI Chatbot Assistant")

SYSTEM_PROMPT = """You are a friendly assistant that helps beginners learn programming.
The user is Greek and often writes in Greeklish (Greek with Latin letters, e.g. "ti kaneis" means "how are you").
Always answer in English, with short and simple sentences,The user's name is Giorgos."""
def web_search(query, max_results=3):
    results = DDGS().text(query, max_results=max_results)
    return "\n".join(f"- {r['title']}: {r['body']}" for r in results)
def make_search_query(question):
    response = ollama.chat(model="qwen2.5:7b", messages=[
        {"role": "system", "content": (
            "Translate the user's message into a short English web search query. "
            "The message may be in any language, including languages written with Latin letters "
            "(for example Greek written as 'posa', 'exei', 'podosfairo' means 'how many', 'has', 'football'). "
            "Keep names as proper names. Reply with ONLY the query.\n\n"
            "Examples:\n"
            "posa protathlimata exei o panathinaikos sto podosfairo -> how many football trophies has Panathinaikos won\n"
            "quel temps fait-il a Paris -> weather in Paris today\n"
            "wer hat die Weltmeisterschaft 2014 gewonnen -> who won the 2014 World Cup\n"
            "cuantos habitantes tiene Madrid -> population of Madrid"
        )},
        {"role": "user", "content": question},
    ])
    return response["message"]["content"].strip().strip('"')


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
        with st.spinner("Searching the web..."):
               search_query = make_search_query(question)
               search_results = web_search(search_query)
        with st.expander("Search results (debug)"):
            st.write("Query:", search_query)
            st.write(search_results)


        system = SYSTEM_PROMPT + "\n\nAnswer ONLY using these web search results. If they do not contain the answer, say you don't know.\n" + search_results
        all_messages = [{"role": "system", "content": system}] + st.session_state.messages

        def stream_answer():
            for chunk in ollama.chat(model="llama3.2", messages=all_messages, stream=True):
                yield chunk["message"]["content"]

        answer = st.write_stream(stream_answer())


    st.session_state.messages.append({"role": "assistant", "content": answer})