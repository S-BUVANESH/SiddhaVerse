import os
import time
from typing import List
from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    def __init__(self, model_name: str = 'intfloat/multilingual-e5-large', device: str = None):
        self.model_name = model_name
        self.device = device
        
        # Load HuggingFace model using SentenceTransformer
        # sentence-transformers handles CUDA availability check automatically if device is None
        t0 = time.time()
        self.model = SentenceTransformer(model_name, device=device)
        self.load_time = time.time() - t0
        self.dimension = self.model.get_embedding_dimension()
        
    def embed_passages(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of document passages. Prepend 'passage: ' instruction for E5 models.
        """
        if not texts:
            return []
        
        # Prepend E5 instructions
        formatted_texts = [f"passage: {t}" for t in texts]
        
        # Generate normalized embeddings
        embeddings = self.model.encode(
            formatted_texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return embeddings.tolist()
        
    def embed_queries(self, queries: List[str]) -> List[List[float]]:
        """
        Embed a list of search queries. Prepend 'query: ' instruction for E5 models.
        """
        if not queries:
            return []
            
        formatted_queries = [f"query: {q}" for q in queries]
        embeddings = self.model.encode(
            formatted_queries,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return embeddings.tolist()

    def get_dimension(self) -> int:
        return self.dimension
