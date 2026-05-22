from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import InMemoryVectorStore
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


loader = PyPDFLoader("temp.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(documents=docs)

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")

vector_db = InMemoryVectorStore.from_documents(
    documents=docs,
    embedding=embeddings
)

llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

def retrieve_context(query: str):
    """Retrieves relevant context from the vector database based on the query."""
    
    context = ""

    docs = vector_db.similarity_search(query=query, k=3)

    for doc in docs:
        context = context + doc.page_content + "\n\n"
    return context

system_prompt = """
You are a helpful AI assistant that answers questions using retrieved document context.
Use the `retrieve_context` tool whenever additional context is needed.
Provide accurate and concise answers.
"""

memory = InMemorySaver()

agent = create_agent(
    model=llm,
    tools=[retrieve_context],
    system_prompt=system_prompt,
    checkpointer=memory
)

while True:
    query = input("User: ")
    if query.lower() in ["exit", "quit"]:
        print("Exiting the agent.")
        break

    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        {"configurable": {"thread_id": "ragagent123"}}
    )
    result = response["messages"][-1].content

    print(f"Agent: {result}")

 