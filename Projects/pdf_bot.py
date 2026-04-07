from dotenv import load_dotenv
import os
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_chroma import Chroma

load_dotenv()

st.title("📚 PDF ChatBot")
st.caption("Ask questions about your uploaded document")

with st.sidebar:
    st.header("Upload your PDF file")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    st.sidebar.success(f"Uploaded: {uploaded_file.name}")

if uploaded_file is None:
    st.info("👈 Upload a PDF from the sidebar to start chatting")
    st.stop()

@st.cache_resource
def build_vectorstore(file):
    with open("temp.pdf", "wb") as f:
        f.write(file.read())

    loader = PyPDFLoader("temp.pdf")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")

    return Chroma.from_documents(chunks, embedding=embeddings)

vector_store = build_vectorstore(uploaded_file)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

def generate_response(query, retriever, llm):
    docs = retriever.invoke(query)
    context = "\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are a precise AI assistant.

Rules:
- Answer ONLY from the context
- If not found → say "I don't know"
- Keep it concise

Context:
{context}

Question:
{query}
"""

    return llm.invoke(prompt).content

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

query = st.chat_input("Ask a question...")

if query:
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    response = generate_response(query, retriever, llm)

    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})