import os
import streamlit as st

from RAG_Functions import *


st.set_page_config(
    page_title="DocWise Assistant.",
    page_icon="📚",
    layout="centered"
)

st.sidebar.title("Navigation")
st.sidebar.write("Welcome to DocWise Assistant! 🚀")


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
    st.info("Doc Procees Completed!")

# Add widget to page for user inputs
user_question = st.text_area("Ask questions from the doc?")

if st.button("Get Answers"):
    answer = answer_Q(user_question)
    st.markdown("### DeepSeek R1")
    st.markdown(answer)