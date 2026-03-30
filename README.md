
# 🧠 Research Paper AI Assistant
 
### *Ask anything. Understand everything.*
 
[![Status](https://img.shields.io/badge/Status-In%20Progress-yellow?style=for-the-badge)](.)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)](.)
[![LangChain](https://img.shields.io/badge/LangChain-Powered-green?style=for-the-badge)](.)
[![Groq](https://img.shields.io/badge/Groq-LLM-orange?style=for-the-badge)](.)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](.)
 
</div>
 
---

## 📌 The Problem
 
Reading research papers is **hard**.
 
A single paper can be 20–50 pages of dense academic text. Researchers, students, and developers spend hours trying to:
 
- Find the **key contributions** buried in the abstract and conclusion
- Understand **complex methodologies** explained in jargon-heavy language
- Cross-reference **specific sections** to answer a targeted question
- Extract **relevant information** without reading the entire paper
 
There is no easy way to just *ask* a paper a question and get a direct, intelligent answer.
 
---

## 💡 The Solution
 
**Research Paper AI Assistant** is a Retrieval-Augmented Generation (RAG) application that lets you upload any research paper (PDF) and have a natural language conversation with it.
 
Upload a paper. Ask a question. Get an intelligent answer — grounded in the actual content of the paper, not hallucinated.
 
```
You:  "What dataset was used to train the model?"
AI:   "The authors used the ImageNet-1K dataset containing 1.2 million
       training images across 1000 classes, as described in Section 4.1
       of the paper."
```
 
No more ctrl+F. No more skimming. Just ask.
 
---

# User Flow 
```
User uploads PDF
      ↓
Extract text from PDF        ← PyMuPDF / pdfplumber
      ↓
Split into chunks             ← LangChain text splitter
      ↓
Embed each chunk              ← HuggingFace all-MiniLM-L6-v2
      ↓
Store vectors in ChromaDB     ← local vector database
      ↓
User asks a question
      ↓
Embed the question            ← same HuggingFace model
      ↓
Semantic search in ChromaDB   ← find top 3 matching chunks
      ↓
Send chunks + question → Groq LLM
      ↓
Final answer returned
```

# Project Structure 
```
research-paper-qa/
│
├── .env                   
├── requirements.txt
├── main.py                
│
├── ingestion/
│   ├── __init__.py
│   ├── pdf_loader.py      
│   └── chunker.py         
│
├── embeddings/
│   ├── __init__.py
│   └── embedder.py        
├── vectorstore/
│   ├── __init__.py
│   └── store.py          
│
├── rag/
│   ├── __init__.py
│   └── pipeline.py        
│
├── uploads/               
└── chroma_db/           
```
