from .embedder import ProductEmbedder
from .vector_store import ProductVectorDB
from .rag_generator import ProductRAGGenerator

class ProductRecommendationPipeline:
    def __init__(self):
        self.vector_db = ProductVectorDB()
        self.rag = ProductRAGGenerator()

    def build_index(self, product_data):
        self.vector_db.build_index(product_data)

    def recommend(self, query_text, top_k=10):
        docs = self.vector_db.search(query_text, top_k=top_k)
        return self.rag.generate(query_text, docs)