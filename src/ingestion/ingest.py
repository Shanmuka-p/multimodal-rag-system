import os
from src.ingestion.document_parser import DocumentParser
from src.ingestion.image_processor import ImageProcessor
from src.ingestion.chunker import TextChunker
from src.embeddings.model_loader import MultimodalEmbedder
from src.vector_store.chroma_manager import ChromaManager

def ingest_documents(source_dir: str = "sample_documents"):
    print(f"Starting ingestion from {source_dir}...")
    
    # Initialize components
    chunker = TextChunker()
    embedder = MultimodalEmbedder()
    db_manager = ChromaManager()
    
    # Loop through all files in the directory
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        
        if filename.endswith(".pdf"):
            print(f"Processing PDF: {filename}...")
            parser = DocumentParser(file_path)
            
            # 1. Extract and Embed Text
            text_data = parser.extract_text()
            for page in text_data:
                chunks = chunker.chunk_text(page["content"])
                for chunk in chunks:
                    embedding = embedder.get_text_embedding(chunk)
                    metadata = {
                        "document_id": filename,
                        "page_number": page["page_number"],
                        "content_type": "text",
                        "content": chunk # Store the actual text in metadata for retrieval
                    }
                    db_manager.add_item(embedding, metadata)
            
            # 2. Extract and Embed Images
            image_data = parser.extract_images()
            for img in image_data:
                embedding = embedder.get_image_embedding(img["file_path"])
                if embedding:
                    metadata = {
                        "document_id": filename,
                        "page_number": img["page_number"],
                        "content_type": "image",
                        "file_path": img["file_path"] # Store path so we can load it later
                    }
                    db_manager.add_item(embedding, metadata)
                    
        elif filename.lower().endswith(('.png', '.jpg', '.jpeg')):
             print(f"Processing Image: {filename}...")
             # For standalone images, we treat the whole image as one item
             embedding = embedder.get_image_embedding(file_path)
             if embedding:
                 metadata = {
                     "document_id": filename,
                     "page_number": 1,
                     "content_type": "image",
                     "file_path": file_path
                 }
                 db_manager.add_item(embedding, metadata)

    print("Ingestion Complete! Database is ready.")

if __name__ == "__main__":
    # Ensure the directory exists
    if not os.path.exists("sample_documents"):
        os.makedirs("sample_documents")
        print("Created sample_documents/ folder. Please add files there and run this again.")
    else:
        ingest_documents()