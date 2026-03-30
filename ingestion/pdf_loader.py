import fitz  # PyMuPDF
import os

def load_pdf(file_path: str) -> str:
    """
    Takes a PDF file path and returns all extracted text as a single string.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF not found at path: {file_path}")

    text = ""
    
    # Open the PDF
    doc = fitz.open(file_path)
    
    # Loop through every page
    for page_num, page in enumerate(doc):
        page_text = page.get_text()
        text += f"\n--- Page {page_num + 1} ---\n"
        text += page_text

    
    
    print(f"✅ Extracted text from {len(doc)} pages")
    doc.close()
    return text
if __name__ == "__main__":
    text = load_pdf("test.pdf")
    print(text[:500])