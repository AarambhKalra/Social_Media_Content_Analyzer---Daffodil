import os
import streamlit as st
from text_extractor import TextExtractor
from gemini_client import analyze_social_media_content

st.set_page_config(
    page_title="Social Media Content Analyzer",
    page_icon="📱",
    layout="wide"
)

st.title("📱 Social Media Content Analyzer")
st.markdown("Upload PDF documents or images of your social media posts to get AI-powered engagement improvement suggestions.")

# Load Gemini API key from Streamlit secrets (if provided)
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

uploaded_file = st.file_uploader(
    "Upload Document (PDF or Image)",
    type=["pdf", "png", "jpg", "jpeg", "gif", "bmp", "tiff"],
    help="Upload a PDF file or image (PNG, JPG, etc.) containing your social media post content"
)

if uploaded_file:
    file_type = uploaded_file.type
    
    # Determine file type and extract text accordingly
    with st.spinner("Extracting text from document..."):
        try:
            if file_type == "application/pdf":
                text = TextExtractor.extract_from_pdf(uploaded_file)
                extraction_method = "PDF Parsing"
            elif file_type.startswith("image/"):
                text = TextExtractor.extract_from_image(uploaded_file)
                extraction_method = "OCR (Optical Character Recognition)"
            else:
                st.error(f"Unsupported file type: {file_type}")
                st.stop()
            
            if not text:
                st.error("No text could be extracted from the document.")
                st.stop()
        except Exception as e:
            st.error(f"Text extraction failed: {e}")
            st.stop()

    # Display extracted text
    with st.expander("📄 Extracted Text", expanded=False):
        st.write(f"**Extraction Method:** {extraction_method}")
        st.text_area("", text, height=150, label_visibility="collapsed", disabled=True)

    # Analyze content
    with st.spinner("🤖 Analyzing content..."):
        try:
            analysis_result = analyze_social_media_content(text)
        except Exception as e:
            st.error(f"Analysis unavailable: {e}")
            st.stop()

    # Display analysis results
    if analysis_result:
        st.subheader("📊 Content Analysis")
        analysis_text = analysis_result.get("analysis", "No analysis available.")
        if analysis_text:
            st.write(analysis_text)
        else:
            st.info("Analysis section is empty.")

