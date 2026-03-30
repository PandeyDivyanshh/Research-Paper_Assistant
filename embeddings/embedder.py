from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_model():
    """
    Loads and returns the HuggingFace embedding model.
    This model converts text into vectors (lists of numbers).
    """
    print("⏳ Loading embedding model...")
    
    model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},   # use "cuda" if you have a GPU
        encode_kwargs={"normalize_embeddings": True}
    )
    
    print("✅ Embedding model loaded!")
    return model


# # ---- TEST BLOCK ----
# if __name__ == "__main__":
#     model = get_embedding_model()

#     # Test with two sentences
#     test_sentences = [
#         "The transformer model uses attention mechanisms.",
#         "Attention helps the model focus on relevant words."
#     ]

#     vectors = model.embed_documents(test_sentences)

#     print(f"\nNumber of vectors: {len(vectors)}")
#     print(f"Vector size: {len(vectors[0])} numbers")
#     print(f"First 5 numbers of vector 1: {vectors[0][:5]}")