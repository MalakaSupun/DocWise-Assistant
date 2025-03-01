import os
import streamlit as st
import re
from RAG_Functions import *

# Set proxy (replace with your actual proxy URL)
PROXY_URL = "http://192.168.4.137:44355"  
os.environ["HTTP_PROXY"] = PROXY_URL
os.environ["HTTPS_PROXY"] = PROXY_URL

st.set_page_config(
    page_title="DocWise Assistant.",
    page_icon="🧩",
    layout="centered"
)

st.sidebar.title("Navigate LLMs 🤖")
st.sidebar.write("Welcome to DocWise 📝 Assistant! 🚀")

st.sidebar.button(label="DeepSeek R1", icon="🐬")
st.sidebar.button(label="mistral-saba-24b", icon='🎯')
st.sidebar.button(label="llama-3.1-70b-versatile", icon='🦙')

# Set the title of the Streamlit app
st.title("DocWise Assistant")

# Create a file uploader widget for PDF files
uploaded_file = st.file_uploader("Upload the Document PDF", type=["pdf"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Define the path to save the uploaded PDF
    save_pdf_path = os.path.join(os.getcwd(), uploaded_file.name)

    # Save the uploaded PDF to the specified path
    with open(save_pdf_path, "wb") as pdf:
        pdf.write(uploaded_file.getbuffer())

    process_docs = process_docs_to_chromaDB(uploaded_file.name)
    st.info("Doc Procees Completed! 🍀 ")

# Add widget to page for user inputs
user_question = st.text_area("Ask questions from the doc?")

if st.button("Get Answers ╰┈➤"):

    # Initialize session state for conversation history
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    # Display conversation history
    for i, (question, answer) in enumerate(st.session_state.conversation):
        st.markdown(f"**Q{i+1}:** {question}")
        st.markdown(f"**A{i+1}:** {answer}")


    answer = answer_Q(user_question)
    st.markdown("### DeepSeek R1")
    s=str(answer)
    
    think_content = re.search(r'<think>(.*?)</think>', s, re.DOTALL).group(1)
    # print(think_content)
    # st.info(think_content)
    with st.expander("See detailed reasoning"):
        st.info(think_content)

    final_answer = re.search(r'</think>\s*(.*)', s, re.DOTALL).group(1)
    # print("Final Anwer:",final_answer)
    st.markdown(final_answer)
    
    
    # # Add the new question and answer to the conversation history
    # if st.button("Get Answers"):
    #     answer = answer_Q(user_question)
    #     st.session_state.conversation.append((user_question, answer))
    #     st.markdown("### DeepSeek R1")
    #     st.markdown(answer)