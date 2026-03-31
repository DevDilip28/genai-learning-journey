from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
import streamlit as st 

llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

st.title("🤖 AskBuddy - Chat Bot")
st.markdown("AskBuddy is a simple chatbot built with LangChain. Ask it anything!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

query = st.chat_input("Ask me anything...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    st.chat_message("user").markdown(query)

    lc_messages = [SystemMessage(content="You are a helpful assistant")]

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            lc_messages.append(HumanMessage(content=msg["content"]))
        else:
            lc_messages.append(AIMessage(content=msg["content"]))

    lc_messages = lc_messages[-12:]

    res = llm.invoke(lc_messages)

    st.chat_message("ai").markdown(res.content)
    st.session_state.messages.append({"role": "ai", "content": res.content})
