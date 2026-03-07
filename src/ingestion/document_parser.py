import fitz  # PyMuPDF
import os

class DocumentParser:
    def __init__(self, file_path: str, output_dir: str = "extracted_assets"):
        self.file_path = file_path
        self.document_id = os.path.basename(file_path)
        self.output_dir = output_dir
        
        # Create a directory to store extracted images
        os.makedirs(self.output_dir, exist_ok=True)

    def extract_text(self):
        """Extracts plain text from a PDF document page by page."""
        extracted_data = []
        try:
            doc = fitz.open(self.file_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text("text")
                if text.strip(): 
                    extracted_data.append({
                        "document_id": self.document_id,
                        "page_number": page_num + 1,
                        "content_type": "text",
                        "content": text.strip()
                    })
            doc.close()
            print(f"Successfully extracted {len(extracted_data)} pages of text from {self.document_id}")
            return extracted_data
        except Exception as e:
            print(f"Error extracting text from {self.file_path}: {e}")
            return []

    def extract_images(self):
        """Extracts embedded images from a PDF and saves them to disk."""
        extracted_images = []
        try:
            doc = fitz.open(self.file_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                image_list = page.get_images(full=True)
                
                for img_index, img in enumerate(image_list):
                    xref = img[0] # The internal PDF reference number for the image
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # Construct a unique filename: doc_name_pageX_imgY.png
                    image_filename = f"{self.document_id}_page{page_num+1}_img{img_index}.{image_ext}"
                    image_filepath = os.path.join(self.output_dir, image_filename)
                    
                    # Save the image to our assets folder
                    with open(image_filepath, "wb") as f:
                        f.write(image_bytes)
                        
                    extracted_images.append({
                        "document_id": self.document_id,
                        "page_number": page_num + 1,
                        "content_type": "image",
                        "file_path": image_filepath # We store the path, not the raw bytes
                    })
            doc.close()
            print(f"Successfully extracted {len(extracted_images)} images from {self.document_id}")
            return extracted_images
        except Exception as e:
            print(f"Error extracting images from {self.file_path}: {e}")
            return []