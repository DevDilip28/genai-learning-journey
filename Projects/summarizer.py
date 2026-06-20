import os
import validators
import streamlit as st

from dotenv import load_dotenv
load_dotenv()

from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_community.document_loaders import UnstructuredURLLoader

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("GROQ_API_KEY not found in .env")
    st.stop()

st.set_page_config(
    page_title="AI URL Summarizer",
    page_icon="🦜"
)

st.title("🦜 AI URL Summarizer")
st.write("Paste a YouTube or Website URL to generate a summary.")

url = st.text_input("Enter URL")


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=groq_api_key
)


prompt = PromptTemplate.from_template("""
You are an expert AI assistant.

Summarize the following content in approximately 300 words.

Content:
{text}
""")


chain = prompt | llm | StrOutputParser()

def get_video_id(youtube_url: str):

    parsed = urlparse(youtube_url)

    if parsed.hostname == "youtu.be":
        return parsed.path[1:]

    if parsed.hostname in (
        "www.youtube.com",
        "youtube.com",
        "m.youtube.com",
    ):
        return parse_qs(parsed.query).get("v", [None])[0]

    return None


if st.button("Generate Summary"):

    if not url.strip():
        st.error("Please enter a URL.")
        st.stop()

    if not validators.url(url):
        st.error("Please enter a valid URL.")
        st.stop()

    try:

        with st.spinner("Loading Content..."):

            # YouTube

            if "youtube.com" in url or "youtu.be" in url:

                video_id = get_video_id(url)

                if not video_id:
                    st.error("Invalid YouTube URL.")
                    st.stop()

                ytt_api = YouTubeTranscriptApi()

                transcript = ytt_api.fetch(video_id)

                text = " ".join(
                    snippet.text
                    for snippet in transcript
                )

            # Website

            else:

                loader = UnstructuredURLLoader(
                    urls=[url],
                    ssl_verify=False,
                    headers={
                        "User-Agent": "Mozilla/5.0"
                    }
                )

                docs = loader.load()

                text = "\n\n".join(
                    doc.page_content
                    for doc in docs
                )

            summary = chain.invoke(
                {
                    "text": text
                }
            )

            st.success(summary)

    except Exception as e:
        st.exception(e)

