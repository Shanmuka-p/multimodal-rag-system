class TextChunker:
    def __init__(self, chunk_size: int = 200, overlap: int = 50):
        # chunk_size is in words, overlap keeps context between chunks
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str) -> list:
        """Splits a long string of text into overlapping chunks."""
        words = text.split()
        chunks = []
        
        if not words:
            return chunks

        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk = " ".join(words[i:i + self.chunk_size])
            chunks.append(chunk)
            
        return chunks