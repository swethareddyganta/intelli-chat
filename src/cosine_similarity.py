import os
import pickle
from sentence_transformers import SentenceTransformer
import tqdm
import json
from typing import List
import numpy as np
from openai import OpenAI

class DocumentSearcher:
    def __init__(self, model_name = 'all-MiniLM-L6-v2', embedding_file = 'embeddings.pkl'):
        self.model = SentenceTransformer(model_name)
        self.embedding_file = embedding_file
        self.corpus_embeddings = None
        self.documents = []

    def index(self, corpus_file: str = "final_scraped.json"):
        if os.path.exists(self.embedding_file):
            print("Loading embeddings from disk...")
            with open(self.embedding_file, 'rb') as f:
                data = pickle.load(f)
                self.corpus_embeddings = data['embeddings']
                self.documents = data['documents']
        else:
            print("Computing embeddings...")
            documents = []
            summaries = []
            revision_ids = []
            with open(corpus_file, 'r', encoding='utf-8') as fp:
                self.data = json.load(fp)
                print(type(self.data))
                # print(self.data[:2])
                print(self.data.keys())
                for key in self.data.keys():
                    for document in tqdm.tqdm(self.data[key]):
                        documents.append({
                            'revision_id': document['revision_id'],
                            'summary': document['summary']
                        })
                        summaries.append(document['summary'])
                        revision_ids.append(document['revision_id'])

            
            # Save documents and compute embeddings for summaries
            self.documents = documents
            self.corpus_embeddings = self.model.encode(summaries, show_progress_bar=True)

            # Save embeddings and documents to disk
            with open(self.embedding_file, 'wb') as f:
                pickle.dump({'embeddings': self.corpus_embeddings, 'documents': self.documents}, f)


    
    def search(self, query: str, top_k: int = 1) -> List[dict]:
        # Embed the query
        query_embedding = self.model.encode(query)
        
        # Calculate cosine similarities
        cosine_similarities = np.dot(self.corpus_embeddings, query_embedding) / \
            (np.linalg.norm(self.corpus_embeddings, axis=1) * np.linalg.norm(query_embedding))
        
        # Get top k indices sorted by similarity (descending order)
        top_indices = cosine_similarities.argsort()[::-1][:top_k]
        
        # Prepare results
        results = [
            {
                'revision_id': self.documents[idx]['revision_id'],
                'summary': self.documents[idx]['summary'],
                'similarity_score': cosine_similarities[idx]
            }
            for idx in top_indices
        ]
        
        return results


# Example usage
def similarity(query):
    # Sample corpus (replace with your actual documents)
    # corpus = [
    #     "Machine learning is a subset of artificial intelligence",
    #     "Deep learning uses neural networks with multiple layers",
    #     "Natural language processing helps computers understand human language",
    #     "Computer vision enables machines to interpret visual information"
    # ]
    
    # Initialize the document searcher
    searcher = DocumentSearcher()
    
    searcher.index()
    # Example query
    # query = "Covid Education"
    
    # Perform search
    results = searcher.search(query)


    result = results[0]
    return result['summary'],result['revision_id']

if __name__ == "__main__":
    print(similarity('skin diseases'))