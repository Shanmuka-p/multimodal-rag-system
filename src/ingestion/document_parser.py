import fitz  # PyMuPDF
import os

class DocumentParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.document_id = os.path.basename(file_path)

    def extract_text(self):
        """
        Extracts plain text from a PDF document page by page.
        Returns a list of dictionaries containing the text and metadata.
        """
        extracted_data = []
        
        try:
            # Open the PDF file
            doc = fitz.open(self.file_path)
            
            # Iterate through each page
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text("text")
                
                # Only save if the page actually contains text
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
            print(f"Error processing document {self.file_path}: {e}")
            return []

# Quick local test (runs only if you execute this specific file)
if __name__ == "__main__":
    # To test this, put a sample PDF in your sample_documents folder
    test_pdf_path = "../../sample_documents/test_doc.pdf"
    
    # Create a dummy file just so the script doesn't crash if you haven't added one yet
    if not os.path.exists("../../sample_documents"):
        os.makedirs("../../sample_documents", exist_ok=True)
        
    if os.path.exists(test_pdf_path):
        parser = DocumentParser(test_pdf_path)
        data = parser.extract_text()
        if data:
            print(f"Sample output from page 1:\n{data[0]}")
    else:
        print(f"Please place a PDF named 'test_doc.pdf' in the sample_documents folder to test.")