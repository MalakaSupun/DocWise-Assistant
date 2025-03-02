import os
import streamlit as st
import re

# Set proxy (replace with your actual proxy URL)
PROXY_URL = "http://192.168.4.137:44355"  
# PROXY_URL = "" 
# os.environ["HTTP_PROXY"] = PROXY_URL
# os.environ["HTTPS_PROXY"] = PROXY_URL

st.set_page_config(
    page_title="DocWise Assistant.",
    page_icon="🧩",
    layout="centered"
)

st.sidebar.title("Navigate LLMs 🤖")
st.sidebar.write("Welcome to DocWise 📝 Assistant! 🚀")
st.sidebar.markdown("Your friendly 🤗 RAG Document Assistant 🤖, here to help you navigate and extract 💚 insights 🌱 from your documents effortlessly. 📄✨")

st.sidebar.markdown("---")  # Add a horizontal line for separation
st.sidebar.header("LLM Selection 🌀")


Model = st.sidebar.radio(
    "Select a suitable LLM for the occasion 🤓",
    options=["DeepSeek R1", "Mistral-saba-24b", "llama-3.2-11b-vision-preview"],
    format_func=lambda x: {
        "DeepSeek R1": "🐬 DeepSeek R1",
        "Mistral-saba-24b": "🎯 Mistral saba",
        "llama-3.2-11b-vision-preview": "🦙 Llama 3.2"
    }[x]
)
# Update query parameters when the radio button is pressed
if "model" not in st.session_state:
    st.session_state.model = Model

if st.session_state.model != Model:
    st.session_state.model = Model
    st.query_params.update({"model":Model})
    print("\n\n Button Press ")
    print(st.query_params['model'],"\n\n\n")

# Move the proxy settings to the bottom of the sidebar
st.sidebar.markdown("---")  # Add a horizontal line for separation
st.sidebar.header("Proxy Settings 🔒")

# Add a text input for the proxy URL
proxy_input = st.sidebar.text_input("Enter Proxy URL 🔑", value=PROXY_URL)

# Update the proxy environment variables if the input is changed
# Add a button to apply the proxy settings
if st.sidebar.button("🕵 Apply Proxy Settings 🕵"):
    if proxy_input != PROXY_URL:    
        os.environ["HTTP_PROXY"] = proxy_input
        os.environ["HTTPS_PROXY"] = proxy_input
        PROXY_URL = proxy_input
        st.sidebar.info("Proxy settings applied successfully!")

# Set the title of the Streamlit app
st.title("DocWise Assistant 🤖")

# Create a file uploader widget for PDF files
uploaded_file = st.file_uploader("Upload the Document PDF", type=["pdf"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Define the path to save the uploaded PDF
    save_pdf_path = os.path.join(os.getcwd(), uploaded_file.name)

    # Save the uploaded PDF to the specified path
    with open(save_pdf_path, "wb") as pdf:
        pdf.write(uploaded_file.getbuffer())
 
    from RAG_Functions import process_docs_to_chromaDB,answer_Q
    
    process_docs = process_docs_to_chromaDB(uploaded_file.name)
    st.success("Document processing completed successfully! 🍀")

# Add widget to page for user inputs
user_question = st.text_area("Ask a question about the document ❔")

if st.button(" 💡 Get Answer ╰┈➤"):

    # Initialize session state for conversation history
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    # Display conversation history
    for i, (question, answer) in enumerate(st.session_state.conversation):
        st.markdown(f"**Q{i+1}:** {question}")
        st.markdown(f"**A{i+1}:** {answer}")


    answer = answer_Q(user_question)
    st.markdown(f"### {Model}")
    if Model == "DeepSeek R1":
        s=str(answer)
        print(s)
        
        think_content = re.search(r'<think>(.*?)</think>', s, re.DOTALL).group(1)
        # print(think_content)
        # st.info(think_content)
        with st.expander("See detailed reasoning"):
            st.info(think_content)

        final_answer = re.search(r'</think>\s*(.*)', s, re.DOTALL).group(1)
        # print("Final Anwer:",final_answer)
        st.markdown(final_answer)

    else:
        st.markdown(answer)

    
  