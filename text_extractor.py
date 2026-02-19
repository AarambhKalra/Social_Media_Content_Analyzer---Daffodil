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
        # On Linux/Mac, check common installation paths
        possible_paths = [
            '/usr/bin/tesseract',
            '/usr/local/bin/tesseract',
            '/usr/share/tesseract-ocr/tesseract',
            '/opt/homebrew/bin/tesseract'  # macOS with Homebrew
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        # If not found, assume it's in PATH
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
            except Exception as version_error:
                # Try to proceed anyway, as sometimes version check fails but OCR works
                print(f"Warning: Tesseract version check failed ({version_error}), attempting OCR anyway...")
            
            # Reset file pointer in case it was read before
            file.seek(0)
            image =Image .open (io .BytesIO (file .read ()))

            text =pytesseract .image_to_string (image )
            if not text.strip():
                raise ValueError("No text was extracted from the image. The image may not contain readable text, or OCR quality is poor.")
            return text .strip ()
        except Exception as e :
            raise ValueError (f"OCR extraction failed: {e }")

