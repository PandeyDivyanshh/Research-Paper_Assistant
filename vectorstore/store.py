import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import chromadb
from chromadb.config import Settings
from embeddings.embedder import get_embedding_model

# Initialize ChromaDB client (saves data locally in chroma_db/ folder)
client = chromadb.PersistentClient(path="chroma_db")

def get_or_create_collection(collection_name: str = "research_papers"):
    """
    Gets existing collection or creates a new one.
    A collection is like a table in a database.
    """
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}  # use cosine similarity for search
    )
    return collection


def store_chunks(chunks: list[str], collection_name: str = "research_papers"):
    """
    Embeds all chunks and stores them in ChromaDB.
    """
    print(f"⏳ Embedding and storing {len(chunks)} chunks...")

    model = get_embedding_model()
    collection = get_or_create_collection(collection_name)

    # Embed all chunks at once
    vectors = model.embed_documents(chunks)

    # Store each chunk with its vector and a unique ID
    collection.add(
        documents=chunks,
        embeddings=vectors,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

    print(f"✅ Stored {len(chunks)} chunks in ChromaDB!")


def search_chunks(query: str, collection_name: str = "research_papers", top_k: int = 3):
    """
    Takes a user question, embeds it, and finds the
    top_k most similar chunks from the vector database.
    """
    print(f"🔍 Searching for: {query}")

    model = get_embedding_model()
    collection = get_or_create_collection(collection_name)

    # Embed the question
    query_vector = model.embed_query(query)

    # Search for most similar chunks
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )

    # Return just the text chunks
    return results["documents"][0]


def reset_collection(collection_name: str = "research_papers"):
    """
    Deletes and recreates the collection.
    Useful when a new PDF is uploaded.
    """
    try:
        client.delete_collection(collection_name)
        print(f"🗑️ Cleared existing collection: {collection_name}")
    except:
        pass
    return get_or_create_collection(collection_name)


# # ---- TEST BLOCK ----
# if __name__ == "__main__":
#     import sys
#     import os
#     sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#     from ingestion.pdf_loader import load_pdf
#     from ingestion.chunker import split_text

#     # Step 1: Load and chunk the PDF
#     text = load_pdf("test.pdf")
#     chunks = split_text(text)

#     # Step 2: Reset old data and store new chunks
#     reset_collection()
#     store_chunks(chunks)

#     # Step 3: Test a search query
#     query = "What is the attention mechanism?"
#     results = search_chunks(query)

#     print(f"\n🔍 Query: {query}")
#     print(f"\n📄 Top {len(results)} matching chunks:\n")
#     for i, chunk in enumerate(results):
#         print(f"--- Result {i+1} ---")
#         print(chunk)
#         print()