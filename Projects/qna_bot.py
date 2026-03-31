from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
import streamlit as st 

llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

st.title("🤖 AskBuddy - Chat Bot")
st.markdown("AskBuddy is a simple chatbot built with LangChain. Ask it anything!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)

query = st.chat_input("Ask me anything...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    st.chat_message("user").markdown(query)

    res = llm.invoke(query)

    st.chat_message("ai").markdown(res.content)  
    st.session_state.messages.append({"role": "ai", "content": res.content}) 
