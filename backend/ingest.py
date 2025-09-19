import PyPDF2
import os
import numpy as np
import faiss
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict

class DocumentIngestor:
    def __init__(self, data_dir="data"):  # This will be /app/data in Docker
        self.data_dir = data_dir
        self.vectorizer = TfidfVectorizer(max_features=300, stop_words='english')
        self.chunks = []
        self.embeddings = []
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                print(f"PDF has {len(reader.pages)} pages")
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    print(f"Processed page {page_num + 1}")
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            raise
        return text
    
    def clean_text(self, text: str) -> str:
        """Basic text cleaning"""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        return text
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
            
            if i + chunk_size >= len(words):
                break
                
        return chunks
    
    def generate_embeddings(self, chunks: List[str]) -> np.ndarray:
        """Generate TF-IDF embeddings"""
        tfidf_matrix = self.vectorizer.fit_transform(chunks)
        return tfidf_matrix.toarray().astype('float32')
    
    def process_documents(self):
        """Process all PDF documents in data directory"""
        print(f"Looking for PDFs in: {os.path.abspath(self.data_dir)}")
        
        # Check if data directory exists
        if not os.path.exists(self.data_dir):
            print(f"Data directory {self.data_dir} does not exist!")
            os.makedirs(self.data_dir, exist_ok=True)
            print(f"Created data directory {self.data_dir}")
            return
        
        pdf_files = [f for f in os.listdir(self.data_dir) if f.endswith('.pdf')]
        print(f"Found PDF files: {pdf_files}")
        
        if not pdf_files:
            print("No PDF files found in data directory!")
            return
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.data_dir, pdf_file)
            print(f"Processing {pdf_path}...")
            
            # Point 2 mentioned in assignment Extract and clean text
            text = self.extract_text_from_pdf(pdf_path)
            cleaned_text = self.clean_text(text)
            print(f"Extracted {len(cleaned_text)} characters")
            
            # Chunk text
            chunks = self.chunk_text(cleaned_text)
            print(f"Created {len(chunks)} chunks")
            self.chunks.extend([{"text": chunk, "source": pdf_file} for chunk in chunks])
        
        if not self.chunks:
            print("No text chunks were created!")
            return
            
        # Generate embeddings for all chunks
        chunk_texts = [chunk["text"] for chunk in self.chunks]
        self.embeddings = self.generate_embeddings(chunk_texts)
        print(f"Generated embeddings of shape: {self.embeddings.shape}")
        
        # point 3 of the assignment - Save chunks and embeddings implemented
        self.save_data()
        
    def save_data(self):
        """Save chunks and FAISS index"""
        # Save chunks metadata
        with open('meta.json', 'w') as f:
            json.dump(self.chunks, f)
        
        # Task 1 - Create and save FAISS index
        dimension = self.embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(self.embeddings)
        faiss.write_index(index, 'faiss_index.bin')
        
        # Save the vectorizer for later use
        import pickle
        with open('vectorizer.pkl', 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        print(f"Saved {len(self.chunks)} chunks and FAISS index")

if __name__ == "__main__":
    ingestor = DocumentIngestor()
    ingestor.process_documents()