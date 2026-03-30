from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(text: str) -> list[str]:
    """
    Splits a large text string into smaller overlapping chunks.
    Returns a list of chunk strings.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,        # Each chunk = max 500 characters
        chunk_overlap=50,      # 50 characters overlap between chunks
        separators=["\n\n", "\n", ".", " "]  # Try to split at natural boundaries
    )

    chunks = splitter.split_text(text)

    print(f"✅ Split into {len(chunks)} chunks")
    return chunks


# ---- TEST BLOCK ----
