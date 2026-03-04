import os
import google.generativeai as genai
from PIL import Image

class VLMGenerator:
    def __init__(self):
        # Configure the Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            # We print a warning but don't crash, helpful for testing without keys
            print("Warning: GEMINI_API_KEY not found in environment variables.")
        else:
            genai.configure(api_key=api_key)
        
        # Initialize Gemini 1.5 Flash (Fast, cheap, and multimodal)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_answer(self, query: str, context_items: list) -> str:
        """
        Constructs a multimodal prompt for Gemini and returns the answer.
        """
        # Gemini accepts a list of "parts" which can be strings or image objects
        prompt_parts = []
        
        # 1. System Instruction
        prompt_parts.append(
            "You are a helpful AI assistant. Answer the user's question using ONLY the provided context below. "
            "If the answer is found in an image, explicitly mention it (e.g., 'As seen in the chart...').\n\n"
        )

        # 2. User Query
        prompt_parts.append(f"User Question: {query}\n\nRetrieved Context:\n")

        # 3. Add Context (Text and Images)
        for item in context_items:
            if item["type"] == "text":
                prompt_parts.append(f"Document Text (Page {item['page']}): {item['content']}\n")
            elif item["type"] == "image":
                try:
                    # Gemini handles PIL Image objects directly!
                    image_path = item["content"]
                    img = Image.open(image_path)
                    
                    prompt_parts.append(f"Image from Page {item['page']}:")
                    prompt_parts.append(img) # We just append the actual image object!
                    prompt_parts.append("\n")
                except Exception as e:
                    print(f"Error loading image for Gemini: {e}")

        try:
            # 4. Generate Content
            response = self.model.generate_content(prompt_parts)
            return response.text
        except Exception as e:
            return f"Error generating answer with Gemini: {e}"