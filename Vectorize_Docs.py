from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Loading the embedding model
embeddings = HuggingFaceEmbeddings()

# Setting up the directory loader to load PDF files from the specified directory
loader = DirectoryLoader(path="Docs",
                          glob="./*.pdf",
                          loader_cls=UnstructuredFileLoader)

# Loading the documents from the directory
documents = loader.load()

# Initializing the text splitter to split documents into chunks
text_splitter = CharacterTextSplitter(chunk_size=2000,
                                      chunk_overlap=500)

# Splitting the loaded documents into text chunks
text_chunks = text_splitter.split_documents(documents)

# Creating a Chroma vector database from the text chunks and embeddings
vectordb = Chroma.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    persist_directory="vector_db_directory"
)

# Printing a message to indicate that the documents have been vectorized
print("Documents Vectorized")