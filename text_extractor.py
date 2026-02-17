import fitz
from PIL import Image
import pytesseract
import io


class TextExtractor:
    """Text extractor supporting PDFs and images (with OCR)."""

    @staticmethod
    def extract_from_pdf(file):
        """Extract text from PDF files using PyMuPDF."""
        try:
            text = ""
            with fitz.open(stream=file.read(), filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
            return text.strip()
        except Exception as e:
            raise ValueError(f"PDF extraction failed: {e}")

    @staticmethod
    def extract_from_image(file):
        """Extract text from image files using OCR (Tesseract)."""
        try:
            # Read image file
            image = Image.open(io.BytesIO(file.read()))
            
            # Perform OCR
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            raise ValueError(f"OCR extraction failed: {e}")

