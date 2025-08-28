import chromadb
from typing import List, Dict, Any
from app.core.config import settings

class ChromaSearchClient:
    def __init__(self):
        self.client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT
        )
        self.collection = self.client.get_or_create_collection("meetings")
    
    def add_documents(self, meeting_id: str, documents: List[str], metadatas: List[Dict[str, Any]] = None):
        """Add documents to the collection"""
        if metadatas is None:
            metadatas = [{"meeting_id": meeting_id} for _ in documents]
        
        ids = [f"{meeting_id}_chunk_{i}" for i in range(len(documents))]
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query: str, meeting_id: str = None, n_results: int = 5):
        """Search for relevant documents"""
        where = {"meeting_id": meeting_id} if meeting_id else None
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )
        
        return {
            "documents": results["documents"][0],
            "metadatas": results["metadatas"][0],
            "ids": results["ids"][0],
            "distances": results["distances"][0] if "distances" in results else []
        }

# Global instance
search_client = ChromaSearchClient()