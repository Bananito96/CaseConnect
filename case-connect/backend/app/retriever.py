# backend/app/retriever.py
from sentence_transformers import SentenceTransformer
import torch
from typing import List, Dict, Optional
from datetime import datetime
import json
import os

class CaseProcessor:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        self.cases_db = self._load_cases()
        self.embeddings_cache = {}
        
    def _load_cases(self) -> Dict:
        """Load cases from JSON files in data directory"""
        cases = {}
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            # Create sample data if none exists
            self._create_sample_data(data_dir)
            
        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
                    cases.update(json.load(f))
        return cases
    
    def _create_sample_data(self, data_dir: str):
        """Create sample case data"""
        sample_cases = {
            "case1": {
                "title": "Mizzi v. Malta",
                "summary": "Case concerning paternity rights and access to court",
                "content": "The Court considers that the fact that the applicant was never allowed to contest his paternity...",
                "jurisdiction": "CODICES",
                "date": "2006-01-12T00:00:00",
            },
            # Add more sample cases here
        }
        
        with open(os.path.join(data_dir, 'sample_cases.json'), 'w', encoding='utf-8') as f:
            json.dump(sample_cases, f, ensure_ascii=False, indent=2)
    
    def compute_embeddings(self, text: str) -> torch.Tensor:
        """Compute embeddings for text"""
        return self.model.encode(text, convert_to_tensor=True)
    
    def search(self, query: str, jurisdictions: List[str],
              date_from: Optional[datetime] = None,
              date_to: Optional[datetime] = None,
              top_k: int = 5) -> List[Dict]:
        """Search for similar cases with filtering"""
        query_embedding = self.compute_embeddings(query)
        results = []
        
        for case_id, case in self.cases_db.items():
            # Apply jurisdiction filter
            if jurisdictions and case['jurisdiction'] not in jurisdictions:
                continue
                
            # Apply date filter
            case_date = datetime.fromisoformat(case['date'])
            if date_from and case_date < date_from:
                continue
            if date_to and case_date > date_to:
                continue
            
            # Compute similarity
            case_embedding = self.compute_embeddings(case['content'])
            similarity = torch.cosine_similarity(query_embedding, case_embedding, dim=0).item()
            
            if similarity > 0.5:  # Threshold for relevance
                results.append({
                    "title": case['title'],
                    "summary": case['summary'],
                    "highlight": self._extract_relevant_excerpt(case['content'], query),
                    "jurisdiction": case['jurisdiction'],
                    "date": case_date,
                    "similarity": similarity
                })
        
        # Sort by similarity and return top_k results
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]
    
    def _extract_relevant_excerpt(self, content: str, query: str, context_words: int = 30) -> str:
        """Extract relevant excerpt from case content"""
        # Simple implementation - could be improved with better NLP techniques
        words = content.split()
        for i in range(len(words)):
            context = ' '.join(words[max(0, i-context_words):min(len(words), i+context_words)])
            if query.lower() in context.lower():
                return f"...{context}..."
        return content[:200] + "..."  # Fallback to first 200 chars
