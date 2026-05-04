from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", streaming=True)
search = GoogleSerperAPIWrapper()
tools = [search.run]

if "memory" not in st.session_state:
    st.session_state.memory = MemorySaver()
    st.session_state.history = [] 


agent = create_agent(
    model=llm,
    tools=tools,
    checkpointer=st.session_state.memory,
    system_prompt="You are a amazing ai chat bot agent that can answer from google also."
)

st.subheader("ChatBot Agent")

for message in st.session_state.history:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)

query = st.chat_input("Ask me anything...")

if query:
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role": "user", "content": query})

    res = agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        {"configurable": {"thread_id": "chatbot123"}},
        stream_mode="messages"
    )

    ai_container = st.chat_message("ai") 

    with ai_container:
        space = st.empty()

        message = ""

        for chunk in res: 
            message = message + chunk[0].content
            space.write(message)

        st.session_state.history.append({"role": "ai", "content": message})
