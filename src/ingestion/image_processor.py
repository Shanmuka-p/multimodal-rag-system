import pytesseract
from PIL import Image
import os

class ImageProcessor:
    def __init__(self, image_path: str):
        self.image_path = image_path

    def extract_text_with_ocr(self):
        """
        Runs Optical Character Recognition (OCR) on an image file.
        Returns a dictionary with the extracted text if any is found.
        """
        try:
            # Open the image using Pillow (PIL)
            img = Image.open(self.image_path)
            
            # Run Tesseract OCR to find text in the image
            text = pytesseract.image_to_string(img)
            
            if text.strip():
                return {
                    "source_image": os.path.basename(self.image_path),
                    "content_type": "image_text",
                    "content": text.strip()
                }
            return None
            
        except FileNotFoundError:
            print(f"Error: Could not find image at {self.image_path}")
            return None
        except pytesseract.TesseractNotFoundError:
            print("Error: Tesseract is not installed or not in your system PATH.")
            return None
        except Exception as e:
            print(f"OCR Error on {self.image_path}: {e}")
            return None