from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

class ProductVectorDB:
    def __init__(self, persist_path="faiss_index"):
        self.persist_path = persist_path
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_store = None

    def build_index(self, products):
        documents = []
        for p in products:
            if not p["description"]:
                continue
            documents.append(Document(
                page_content=p["description"],
                metadata={
                    "title": p["title"],
                    "brand": p["brand"],
                    "url": p["url"]
                }
            ))
        self.vector_store = FAISS.from_documents(documents, self.embedding_model)
        self.vector_store.save_local(self.persist_path)

    def load_index(self):
        self.vector_store = FAISS.load_local(self.persist_path, self.embedding_model)

    def search(self, query_text, top_k=5):
        if not self.vector_store:
            self.load_index()
        return self.vector_store.similarity_search(query_text, k=top_k)