import numpy as np
from typing import Dict, List, Optional
import json
import os

class EmbeddingManager:
    def __init__(self, base_path: str = "./data/embeddings"):
        self.base_path = base_path
        self.embeddings_data = {}
        self.load_embeddings()
    
    def load_embeddings(self):
        """Load embeddings and metadata from disk"""
        for dataset in os.listdir(self.base_path):
            dataset_path = os.path.join(self.base_path, dataset)
            if os.path.isdir(dataset_path):
                try:
                    embeddings_file = os.path.join(dataset_path, "embeddings_final.npy")
                    metadata_file = os.path.join(dataset_path, "metadata_final.json")
                    
                    if os.path.exists(embeddings_file) and os.path.exists(metadata_file):
                        embeddings = np.load(embeddings_file)
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                            
                        self.embeddings_data[dataset] = {
                            "embeddings": embeddings,
                            "metadata": metadata
                        }
                        print(f"Loaded {dataset} with {len(metadata)} documents")
                except Exception as e:
                    print(f"Error loading {dataset}: {str(e)}")
    
    def search(self, 
               query_embedding: np.ndarray, 
               top_k: int = 5,
               jurisdictions: Optional[List[str]] = None,
               date_range: Optional[Dict] = None) -> List[Dict]:
        """Search for similar documents"""
        results = []
        
        for dataset, content in self.embeddings_data.items():
            if jurisdictions and dataset not in jurisdictions:
                continue
            
            similarities = np.dot(query_embedding, content["embeddings"].T).flatten()
            top_indices = similarities.argsort()[-top_k:][::-1]
            
            for idx in top_indices:
                metadata = content["metadata"][idx]
                
                if date_range:
                    doc_date = metadata.get("date")
                    if doc_date:
                        if date_range.get("from") and doc_date < date_range["from"]:
                            continue
                        if date_range.get("to") and doc_date > date_range["to"]:
                            continue
                
                results.append({
                    "dataset": dataset,
                    "similarity": float(similarities[idx]),
                    "metadata": metadata
                })
        
        return sorted(results, key=lambda x: x["similarity"], reverse=True)[:top_k]
