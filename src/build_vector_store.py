# 3_build_vector_store.py
# Create local vector database (RAG) from compliance policies

import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define paths
policy_folder = 'data/compliance_policies/'
persist_directory = 'data/compliance_rag_db/'

# Create embedding function
embedding = OpenAIEmbeddings()

# Step 1: Load all compliance policy documents
loaders = []
for filename in os.listdir(policy_folder):
    if filename.endswith('.txt'):
        loaders.append(TextLoader(os.path.join(policy_folder, filename)))

documents = []
for loader in loaders:
    documents.extend(loader.load())

print(f"Loaded {len(documents)} documents from {policy_folder}")

# Step 2: Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
split_docs = text_splitter.split_documents(documents)

print(f"Split into {len(split_docs)} document chunks.")

# Step 3: Create and persist the vectorstore
vectordb = Chroma.from_documents(
    documents=split_docs,
    embedding=embedding,
    persist_directory=persist_directory
)
vectordb.persist()

print(f"Vector store created and saved in {persist_directory}.")
