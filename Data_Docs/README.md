#
<p align="center">
       <img width="1024" src='../Images/Logo_02.png' alt="Logo">
</p>
<h1 align="center">
Add PDF to this folder.
</h1>


## How Chroma Vectorizes a PDF File

Chroma uses a multi-step process to vectorize a PDF file:

1. **PDF Parsing**: The PDF file is parsed to extract text and images. This is typically done using libraries such as PyMuPDF or PDFMiner.

2. **Text Extraction**: The extracted text is cleaned and preprocessed. This may involve removing stop words, stemming, and lemmatization.

3. **Tokenization**: The cleaned text is tokenized into words or subwords using a tokenizer.

4. **Embedding Generation**: Each token is converted into a vector representation using pre-trained models like BERT, GPT, or custom embeddings.

5. **Vector Aggregation**: The individual token vectors are aggregated to form a single vector representation for the entire document. This can be done using techniques like averaging, max pooling, or attention mechanisms.

6. **Storage**: The resulting vector is stored in a vector database for efficient retrieval and similarity search.

By following these steps, Chroma effectively converts the content of a PDF file into a numerical vector that can be used for various downstream tasks such as document classification, clustering, and search.
