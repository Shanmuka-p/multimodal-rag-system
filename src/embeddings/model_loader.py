from sentence_transformers import SentenceTransformer
from PIL import Image

class MultimodalEmbedder:
    def __init__(self, model_name: str = "clip-ViT-B-32"):
        print(f"Loading multimodal model: {model_name}...")
        # SentenceTransformer automatically handles downloading and caching the model
        self.model = SentenceTransformer(model_name)

    def get_text_embedding(self, text: str) -> list:
        """Converts text into a vector embedding."""
        # encode() returns a numpy array, we convert to list for the database
        return self.model.encode(text).tolist()

    def get_image_embedding(self, image_path: str) -> list:
        """Converts an image file into a vector embedding."""
        try:
            image = Image.open(image_path)
            return self.model.encode(image).tolist()
        except FileNotFoundError:
            print(f"Error: Image not found at {image_path}")
            return []
        except Exception as e:
            print(f"Error embedding image {image_path}: {e}")
            return []