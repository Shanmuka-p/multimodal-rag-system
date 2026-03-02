import chromadb
import uuid
import os

class ChromaManager:
    def __init__(self, persist_directory: str = "./chroma_db"):
        # This will create a local folder to save your database
        os.makedirs(persist_directory, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # We use 'cosine' similarity because it works best for CLIP embeddings
        self.collection = self.client.get_or_create_collection(
            name="multimodal_rag",
            metadata={"hnsw:space": "cosine"}
        )

    def add_item(self, embedding: list, metadata: dict, item_id: str = None):
        """Adds a single vector and its metadata to the database."""
        if not embedding:
            return None
            
        if item_id is None:
            item_id = str(uuid.uuid4()) # Generate a random unique ID
            
        # Chroma expects lists, even for single items
        self.collection.add(
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[item_id]
        )
        return item_id