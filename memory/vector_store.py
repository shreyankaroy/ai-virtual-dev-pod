"""
ChromaDB vector memory store for the AI Dev Pod.
Stores and retrieves artifact embeddings for cross-run context.
"""

import chromadb
import os


class VectorStore:
    """Simple ChromaDB wrapper for artifact storage and retrieval."""

    def __init__(self, collection_name="dev_pod_artifacts"):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromadb_store")
        self._client = chromadb.PersistentClient(path=db_path)
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add(self, doc_id: str, text: str, metadata: dict = None):
        """Store a document embedding. Upserts if doc_id already exists."""
        if not text or not text.strip():
            return
        self._collection.upsert(
            ids=[doc_id],
            documents=[text[:8000]],
            metadatas=[metadata or {}],
        )

    def query(self, text: str, n_results: int = 3) -> list:
        """Retrieve the most relevant past documents."""
        if self._collection.count() == 0:
            return []
        results = self._collection.query(
            query_texts=[text],
            n_results=min(n_results, self._collection.count()),
        )
        docs = []
        for i, doc in enumerate(results["documents"][0]):
            docs.append({
                "id": results["ids"][0][i],
                "text": doc,
            })
        return docs

    def get_context(self, query: str) -> str:
        """Get a formatted context string from past runs."""
        results = self.query(query, n_results=3)
        if not results:
            return "No previous project context available."
        parts = [f"[{r['id']}]: {r['text'][:500]}" for r in results]
        return "\n\n".join(parts)
