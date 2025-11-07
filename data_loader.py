import json
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import config

class DataLoader:
    def __init__(self, google_api_key):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            google_api_key=google_api_key
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
        )
    
    def load_essays(self, json_path='data/raw/essays.json'):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def create_documents(self, essays_data):
        documents = []
        
        for essay in essays_data:
            doc = Document(
                page_content=essay['content'],
                metadata={
                    'title': essay['title'],
                    'url': essay['url'],
                    'source': essay['source']
                }
            )
            documents.append(doc)
        
        return documents
    
    def chunk_documents(self, documents):
        return self.text_splitter.split_documents(documents)
    
    def create_vectorstore(self, chunks):
        vectorstore = FAISS.from_documents(chunks, self.embeddings)
        return vectorstore
    
    def save_vectorstore(self, vectorstore, path='data/processed/vectorstore'):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        vectorstore.save_local(path)
        print(f"Vectorstore saved to {path}")
    
    def load_vectorstore(self, path='data/processed/vectorstore'):
        return FAISS.load_local(path, self.embeddings, allow_dangerous_deserialization=True)
    
    def build_knowledge_base(self, json_path='data/raw/essays.json'):
        print("Loading essays...")
        essays = self.load_essays(json_path)
        print(f"Loaded {len(essays)} essays")
        
        print("Creating documents...")
        documents = self.create_documents(essays)
        
        print("Chunking documents...")
        chunks = self.chunk_documents(documents)
        print(f"Created {len(chunks)} chunks")
        
        print("Creating vectorstore (this may take a few minutes)...")
        vectorstore = self.create_vectorstore(chunks)
        
        print("Saving vectorstore...")
        self.save_vectorstore(vectorstore)
        
        return vectorstore

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("Please set GOOGLE_API_KEY environment variable")
        exit(1)
    
    loader = DataLoader(api_key)
    loader.build_knowledge_base()