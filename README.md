# Social Media Content Analyzer

A Streamlit application that analyzes social media posts and suggests engagement improvements using AI-powered content analysis.

## URL

https://socialmediacontentanalyzer-daffodil.streamlit.app/

## Features

### 1. Document Upload

- **PDF Support**: Upload PDF files containing social media content
- **Image Support**: Upload image files (PNG, JPG, JPEG, GIF, BMP, TIFF) including scanned documents
- **Drag-and-Drop Interface**: Easy file upload via Streamlit's file picker

### 2. Text Extraction

- **PDF Parsing**: Extracts text from PDFs using PyMuPDF while maintaining formatting
- **OCR (Optical Character Recognition)**: Extracts text from images using Tesseract OCR for scanned documents and screenshots

### 3. AI-Powered Analysis

- **Content Analysis**: Analyzes tone, message clarity, and target audience
- **Engagement Suggestions**: Provides actionable recommendations for improving engagement including:
  - Hashtag recommendations
  - Call-to-action improvements
  - Content structure optimization
  - Timing and posting strategies

## Technical Requirements

- **Clean, production-quality code**: Well-structured, modular codebase
- **Error handling**: Comprehensive error handling for file uploads, text extraction, and API calls
- **Loading states**: User-friendly loading indicators during processing
- **Documentation**: Clear README and inline code documentation

## Setup

### Prerequisites

1. **Python 3.9+**
2. **Tesseract OCR**:
   - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki) and add to PATH
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr tesseract-ocr-eng`
   - **Streamlit Cloud**: Automatically installed via `packages.txt`

### Installation

1. Create virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Configure Gemini API key:

Create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "AIza..."
GEMINI_MODEL = "gemini-3-flash-preview"
```

Or use `.env` file with PowerShell helper:

```powershell
copy .env.sample .env    # edit .env to add your Gemini API key
.\set_env.ps1           # loads .env into current PowerShell session
```

4. Run the application:

```powershell
streamlit run app.py
```

## Usage

1. Upload a PDF or image file containing your social media post
2. Wait for text extraction (PDF parsing or OCR)
3. Review the extracted text
4. Get AI-powered analysis and engagement improvement suggestions

## Project Structure

```
Assignment/
├── app.py                 # Main Streamlit application
├── text_extractor.py       # PDF and OCR text extraction
├── gemini_client.py        # Gemini API integration for content analysis
├── requirements.txt       # Python dependencies
├── packages.txt           # System packages for deployment
├── README.md              # Project documentation
├── .streamlit/
│   └── secrets.toml       # API keys (not committed)
└── tests/
    └── test_gemini_client.py  # Unit tests
```

## Technologies Used

- **Streamlit**: Web application framework
- **PyMuPDF (fitz)**: PDF text extraction
- **Tesseract OCR (pytesseract)**: Image text extraction
- **Google Gemini API**: AI-powered content analysis
- **Pillow (PIL)**: Image processing

## Notes

- Keep API keys secret and do not commit `.streamlit/secrets.toml` to source control
- Tesseract OCR must be installed separately on your system
- The app uses `gemini-3-flash-preview` by default for analysis
- Test data can be collected from public social media sources
