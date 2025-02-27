import os
import json

from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

print("Starting ...")

Working_dir = os.path.dirname(os.path.abspath((__file__)))
config_data = json.load(open(f"{Working_dir}/config.json"))
print(config_data)

GROQ_API_KEY = config_data["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = GROQ_API_KEY


# Loading Embedding model..
embeddings = HuggingFaceEmbeddings()

# Load LLM..

llm_01 = ChatGroq(model="llama-3.1-70b-versatile",temperature=0)
llm_02 = ChatGroq(model="mistral-saba-24b", temperature=0)
llm_03 = ChatGroq(model="deepseek-r1-distill-llama-70b", temperature=0)


def process_docs_to_chromaDB(file_name):
    loader = UnstructuredPDFLoader(f"{Working_dir}/{file_name}")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    vector_DB = Chroma.from_documents(documents=texts, embedding=embeddings,persist_directory=f"{Working_dir}/doc_vector_store")
    return 0

def answer_Q(user_quections):
    vectordb = Chroma(
        persist_directory=f"{Working_dir}/doc_vector_store",
        embedding_function=embeddings
    )
    Retriever = vectordb.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(
        llm = llm_03,
        chain_type="stuff",
        retriever= Retriever,
        return_source_documents=True
    )

    responce = qa_chain.invoke({"query":user_quections})
    answer = responce("result")

    return answer
