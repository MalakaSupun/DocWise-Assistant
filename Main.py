
# Main script for the DocWise Assistant application.

# This script sets up a Streamlit web application that allows users to interact with a conversational AI model.
# The application uses various libraries including Streamlit, LangChain, and HuggingFace for embeddings.

# Functions:
#     setup_vectorstore(): Initializes and returns a Chroma vector store with HuggingFace embeddings.
#     chat_chain(vectorstore): Sets up and returns a ConversationalRetrievalChain using the provided vector store.

# Streamlit UI Elements:
#     - Page configuration and title.
#     - Chat history management.
#     - User input handling.
#     - Display of chat messages.

# Environment Variables:
#     - GROQ_API_KEY: API key for accessing the Groq model.

# Configuration:
#     - Reads configuration data from 'config.json' located in the same directory as this script.

import json
import os

import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

print("Done loading libraries....")

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
GROQ_API_KEY = config_data["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = GROQ_API_KEY


def setup_vectorstore():
    persist_directory = f"{working_dir}/vector_db_dir"
    embeddings = HuggingFaceEmbeddings()
    vectorstore = Chroma(persist_directory=persist_directory,
                         embedding_function=embeddings)
    return vectorstore


def chat_chain(vectorstore):
    llm = ChatGroq(model="llama-3.1-70b-versatile",
                   temperature=0)
    retriever = vectorstore.as_retriever()
    memory = ConversationBufferMemory(
        llm=llm,
        output_key="answer",
        memory_key="chat_history",
        return_messages=True
    )
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        memory=memory,
        verbose=True,
        return_source_documents=True
    )

    return chain

    st.markdown(
        """
        <style>
        .main {
            background-color: #0e1117;
            color: #c9d1d9;
        }
        .stButton>button {
            background-color: #21262d;
            color: #c9d1d9;
        }
        .stTextInput>div>div>input {
            background-color: #21262d;
            color: #c9d1d9;
        }
        .stTextArea>div>div>textarea {
            background-color: #21262d;
            color: #c9d1d9;
        }
        .stMarkdown {
            color: #c9d1d9;
        }
        .stChatMessage {
            background-color: #21262d;
            color: #c9d1d9;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
st.set_page_config(
    page_title="DocWise Assistant.",
    page_icon = "📚",
    layout="centered"
)

st.title("📚 DocWise Assistant..")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = setup_vectorstore()

if "conversationsal_chain" not in st.session_state:
    st.session_state.conversationsal_chain = chat_chain(st.session_state.vectorstore)


for message in st.session_state.chat_history: 
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask AI...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)


    with st.chat_message("assistant"):
        response = st.session_state.conversationsal_chain({"question": user_input})
        assistant_response = response["answer"]
        st.markdown(assistant_response)
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
