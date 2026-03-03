from src.embeddings.model_loader import MultimodalEmbedder
from src.vector_store.chroma_manager import ChromaManager

class Retriever:
    def __init__(self):
        # We reuse the same embedder and DB manager we built yesterday
        self.embedder = MultimodalEmbedder()
        self.db_manager = ChromaManager()

    def query(self, text_query: str, top_k: int = 5):
        """
        Searches the vector database for the most relevant text and images.
        """
        print(f"Retrieving context for query: '{text_query}'...")
        
        # 1. Convert the user's text query into a vector
        query_embedding = self.embedder.get_text_embedding(text_query)
        
        # 2. Search the database for the 'nearest neighbors' (most similar vectors)
        results = self.db_manager.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["metadatas", "documents", "distances"]
        )
        
        # 3. Format the results into a clean list
        structured_results = []
        
        # Chroma returns a list of lists (because you can query multiple things at once)
        # We only queried one thing, so we look at index 0.
        if results and results['metadatas']:
            for i in range(len(results['metadatas'][0])):
                meta = results['metadatas'][0][i]
                score = results['distances'][0][i] # Distance score (lower is better for cosine)
                
                # We identify if it's text or image based on the metadata we saved earlier
                item = {
                    "type": meta.get("content_type", "unknown"),
                    "page": meta.get("page_number", 0),
                    "source": meta.get("document_id", "unknown"),
                    "score": score
                }
                
                if item["type"] == "text":
                    item["content"] = results['documents'][0][i]
                elif item["type"] == "image":
                    item["content"] = meta.get("file_path", "") # For images, content is the path
                    
                structured_results.append(item)
                
        return structured_results

# Quick test block
if __name__ == "__main__":
    retriever = Retriever()
    # This won't return anything real unless you've actually ingested documents first!
    results = retriever.query("test query")
    print(f"Found {len(results)} results.")