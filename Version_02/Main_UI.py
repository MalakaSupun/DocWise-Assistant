import os
import streamlit as st
import re
import shelve



# Set proxy (replace with your actual proxy URL)
PROXY_URL = "http://192.168.101.243:44355"  

st.set_page_config(
    page_title="DocWise Assistant.",
    page_icon="🧩",
    layout="centered"
)

USER_AVATAR = "👤"
# BOT_AVATAR = "🤖"

BOT_AVATARS = {
    "DeepSeek R1": "🐬",
    "Mistral-saba-24b": "🎯",
    "llama-3.2-11b-vision-preview": "🦙"
}

# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

# Save chat history to shelve file
def save_chat_history(messages):
    # clean_messages = []
    # for msg in messages:
    #     if isinstance(msg, re.Match):
    #         clean_messages.append(msg.group(1))  # Store the matched text, not the object
    #     else:
    #         clean_messages.append(msg)

    with shelve.open("chat_history") as db:
        db["messages"] = messages


# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

st.sidebar.title("Navigate LLMs 🤖")
st.sidebar.write("Welcome to DocWise 📝 Assistant! 🚀")
st.sidebar.write("---")

def format_model(model_name):
    return f"{BOT_AVATARS[model_name]} {model_name}"

# st.sidebar.markdown("---")  # Add a horizontal line for separation
st.sidebar.header("LLM Selection 🌀")
Model = st.sidebar.radio(
    "Select a suitable LLM for the occasion 🤓",
    options=list(BOT_AVATARS.keys()),
    format_func=format_model
)
# Dynamically update BOT_AVATAR based on selection
BOT_AVATAR = BOT_AVATARS[Model]

# Update query parameters when the radio button is pressed
if "model" not in st.session_state:
    st.session_state.model = Model

if st.session_state.model != Model:
    st.session_state.model = Model
    st.query_params.update({"model":Model})
    # print("\n\n Button Press ")
    # print(st.query_params['model'],"\n\n\n")

st.sidebar.markdown("---")  # Add a horizontal line for separation
st.sidebar.header("⏳ History ⏳")
st.sidebar.write("🧹 Clear the history 🌱 of this conversation 🍀 and start fresh... 🌟")

# Sidebar with a button to delete chat history
if st.sidebar.button("🗑️ Delete Chat History 🚮"):
    st.session_state.messages = []
    save_chat_history([])

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
st.markdown("Your friendly 🤗 RAG Document Assistant 🤖, here to help you navigate and extract 💚 insights 🌱 from your documents effortlessly. 📄✨")

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

# Display the LLM model used for each question
for message in st.session_state.messages:

    if message["role"] == "user":
        with st.chat_message("user",avatar=USER_AVATAR):
            st.info(f"**{message['content']}**")
    else:
        icon = f"{message['icon']}"
        # print(icon,type(icon))
        with st.chat_message("assistant",avatar=icon ):
            st.markdown(f"**({message['LLM']}):** {message['content']}")

 # User input
if user_question := st.chat_input("Ask a question about the document ❔"):
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    from RAG_Functions import answer_Q, process_docs_to_chromaDB,answer_Q
    answer = answer_Q(user_question)
    
    with st.chat_message("assistant",avatar=BOT_AVATAR):
        if Model == "DeepSeek R1":
            s = str(answer)
         
            think_match = re.search(r'<think>(.*?)</think>', s, re.DOTALL)
            final_answer_match = re.search(r'</think>\s*(.*)', s, re.DOTALL)
            
            final_answer_match = str(final_answer_match.group(1))
            # print("\n\n\n", final_answer_match , "\n\n\n")
            if think_match:
                with st.expander("See detailed reasoning"):
                    st.info(think_match.group(1))
            if final_answer_match:
                st.markdown(final_answer_match)
            # print(final_answer_match)    
            st.session_state.messages.append({"role": "assistant","LLM": Model,"icon":BOT_AVATAR, "content": final_answer_match})

        else:
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant","LLM": Model,"icon":BOT_AVATAR, "content": answer})
    
    
    save_chat_history(st.session_state.messages)

    