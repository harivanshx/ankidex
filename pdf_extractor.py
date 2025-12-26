"""
PDF Text Extraction Module
Extracts text content from PDF files using PyMuPDF
"""

import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text content from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as a single string
    """
    text_content = []
    
    try:
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():
                text_content.append(text)
        
        doc.close()
        
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    return "\n\n".join(text_content)


def extract_text_from_bytes(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF bytes (for file uploads).
    
    Args:
        pdf_bytes: PDF file content as bytes
        
    Returns:
        Extracted text as a single string
    """
    text_content = []
    
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():
                text_content.append(text)
        
        doc.close()
        
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    return "\n\n".join(text_content)
