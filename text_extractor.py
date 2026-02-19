import fitz 
from PIL import Image 
import pytesseract 
import io 

# Set the path to tesseract executable - will be auto-detected on most systems
# On Windows, it might be at 'C:\Program Files\Tesseract-OCR\tesseract.exe'
# On Linux/Mac, it's usually in PATH
try:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
except:
    # On deployment platforms, Tesseract should be in PATH
    pass


class TextExtractor :
    """Text extractor supporting PDFs and images (with OCR)."""

    @staticmethod 
    def extract_from_pdf (file ):
        """Extract text from PDF files using PyMuPDF."""
        try :
            text =""
            with fitz .open (stream =file .read (),filetype ="pdf")as doc :
                for page in doc :
                    text +=page .get_text ()
            return text .strip ()
        except Exception as e :
            raise ValueError (f"PDF extraction failed: {e }")

    @staticmethod 
    def extract_from_image (file ):
        """Extract text from image files using OCR (Tesseract)."""
        try :

            image =Image .open (io .BytesIO (file .read ()))


            text =pytesseract .image_to_string (image )
            return text .strip ()
        except Exception as e :
            raise ValueError (f"OCR extraction failed: {e }")

