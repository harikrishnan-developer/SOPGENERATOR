
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

import os
import re

# --- Helper function to clean text ---
def clean_text(text):
    # Collapse multiple newlines
    text = re.sub(r'\n{2,}', '\n', text)
    # Remove page numbers like "Page X of Y"
    text = re.sub(r'Page \d+ of \d+', '', text)
    # Optional: Remove leading/trailing whitespace
    text = text.strip()
    return text

# --- Load and split documents ---
def load_and_split_documents(data_dir):
    docs = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            try:
                loader = TextLoader(os.path.join(data_dir, filename))
                loaded_docs = loader.load()
                
                # Clean text in each document
                for doc in loaded_docs:
                    doc.page_content = clean_text(doc.page_content)
                
                docs.extend(loaded_docs)
                print(f"Loaded and cleaned: {filename}")
            except Exception as e:
                print(f"Failed to load {filename}: {e}")
    
    # Use recursive splitter for better structure
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(docs)
    print(f"Total split documents: {len(split_docs)}")
    
    return split_docs

# --- Create and populate vector store ---
def create_and_populate_vector_store(docs, persist_dir):
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if not os.path.exists(persist_dir) or not os.listdir(persist_dir):
        db = Chroma.from_documents(docs, embedder, persist_directory=persist_dir)
        print("Vector DB created and persisted!")
    else:
        db = Chroma(persist_directory=persist_dir, embedding_function=embedder)
        print("Loaded existing Vector DB.")
    
    return db

# --- Main block for running standalone ---
if __name__ == "__main__":
    data_dir = '/content/drive/MyDrive/agentic_sop_project/data/'
    persist_dir = '/content/drive/MyDrive/agentic_sop_project/chromadb/'
    
    docs = load_and_split_documents(data_dir)
    create_and_populate_vector_store(docs, persist_dir)
