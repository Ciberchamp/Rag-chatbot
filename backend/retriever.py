import faiss
import numpy as np
import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict

class Retriever:
    def __init__(self, index_path="faiss_index.bin", meta_path="meta.json", vectorizer_path="vectorizer.pkl"):
        self.index = faiss.read_index(index_path)
        with open(meta_path, 'r') as f:
            self.metadata = json.load(f)
        with open(vectorizer_path, 'rb') as f:
            self.vectorizer = pickle.load(f)
        
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for most relevant documents"""
        # Generate query embedding using TF-IDF
        query_vec = self.vectorizer.transform([query]).toarray().astype('float32')
        
        # Task 2 - Search in FAISS index
        distances, indices = self.index.search(query_vec, top_k)
        
        # Retrieve relevant documents
        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        
        # Simple re-ranking by text similarity
        results = self.rerank_results(query, results)
        
        return results[:top_k]
    
    def rerank_results(self, query: str, results: List[Dict]) -> List[Dict]:
        """Simple re-ranking based on term frequency"""
        query_terms = query.lower().split()
        
        def score_doc(doc):
            text = doc['text'].lower()
            score = 0
            for term in query_terms:
                # Simple term frequency scoring
                score += text.count(term)
            return score
        
        # Sort by score descending
        return sorted(results, key=score_doc, reverse=True)