# Research-Paper_Assistant





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
