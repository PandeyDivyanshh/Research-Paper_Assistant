import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from ingestion.pdf_loader import load_pdf
from ingestion.chunker import split_text
from vectorstore.store import store_chunks, reset_collection
from rag.pipeline import answer_question

load_dotenv()

app = FastAPI(title="Research Paper AI Assistant")


# ---- Request model for /ask ----
class QuestionRequest(BaseModel):
    question: str


# ---- Root endpoint ----
@app.get("/")
def root():
    return {"message": "Research Paper AI Assistant is running!"}


# ---- Upload endpoint ----
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Accepts a PDF file, extracts text, chunks it,
    embeds it and stores in ChromaDB.
    """
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # Save uploaded file to uploads/ folder
    upload_path = f"uploads/{file.filename}"
    with open(upload_path, "wb") as f:
        content = await file.read()
        f.write(content)

    print(f"✅ PDF saved to {upload_path}")

    # Process the PDF
    text = load_pdf(upload_path)
    chunks = split_text(text)

    # Clear old data and store new chunks
    reset_collection()
    store_chunks(chunks)

    return {
        "message": "PDF processed successfully!",
        "filename": file.filename,
        "chunks_stored": len(chunks)
    }


# ---- Ask endpoint ----
@app.post("/ask")
def ask_question(request: QuestionRequest):
    """
    Accepts a question and returns an AI-generated
    answer based on the uploaded research paper.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    answer = answer_question(request.question)

    return {
        "question": request.question,
        "answer": answer
    }