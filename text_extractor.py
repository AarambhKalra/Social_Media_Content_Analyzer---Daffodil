import fitz 
from PIL import Image 
import pytesseract 
import io 
import os
import platform


def _get_tesseract_cmd():
    """Get the path to tesseract executable based on the platform."""
    system = platform.system().lower()
    
    if system == "windows":
        # Common Windows installation paths
        possible_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            r'C:\Users\%USERNAME%\AppData\Local\Tesseract-OCR\tesseract.exe'
        ]
        for path in possible_paths:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                return expanded_path
        # If not found, let pytesseract try to find it
        return None
    else:
        # On Linux/Mac, assume it's in PATH
        return None


# Set the path to tesseract executable
tesseract_cmd = _get_tesseract_cmd()
if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd


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
            # Check if tesseract is available
            try:
                version = pytesseract.get_tesseract_version()
            except Exception:
                raise ValueError("Tesseract OCR is not installed or not accessible. Please install Tesseract OCR and ensure it's in your PATH, or check the README for installation instructions.")
            
            # Reset file pointer in case it was read before
            file.seek(0)
            image =Image .open (io .BytesIO (file .read ()))

            text =pytesseract .image_to_string (image )
            return text .strip ()
        except Exception as e :
            raise ValueError (f"OCR extraction failed: {e }")

