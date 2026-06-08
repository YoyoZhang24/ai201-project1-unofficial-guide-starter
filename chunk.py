import os
from config import DOCS_PATH
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents():
    """Load all .txt documents from the docs folder."""
    documents = []
    for filename in sorted(os.listdir(DOCS_PATH)):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCS_PATH, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            source_name = filename.replace(".txt", "").replace("_", " ").title()
            documents.append({
                "source": source_name,
                "filename": filename,
                "text": text,
            })
    print(f"Loaded {len(documents)} source document(s): {[d['source'] for d in documents]}")
    return documents

def chunk_document(text, source_name):
    """
    Split a document into chunks ready for embedding.

    Strategy: character-based sliding window with overlap.
     
    Returns a list of dicts, each with:
      - "text"     : the chunk text (str)
      - "source"     : the source name, e.g. "Chicago Maroon" (str)
      - "chunk_id" : a unique identifier, e.g. "chicago_maroon_1", "chicago_maroon_2" (str)
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    texts = [t for t in splitter.split_text(text) if len(t) >= 50]
    prefix = source_name.lower().replace(" ", "_")
    
    return [
        {
            "text": chunk,
            "source": source_name,
            "chunk_id": f"{prefix}_{i}",
        }
        for i, chunk in enumerate(texts)
    ]

def save_chunks_readable(all_chunks, output_path="chunks_preview.txt"):
    """
    Save all chunks to a human-readable text file for inspection
    before converting to embeddings.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(all_chunks):
            f.write(f"{'='*60}\n")
            f.write(f"Chunk #{i+1} | ID: {chunk['chunk_id']} | Source: {chunk['source']}\n")
            f.write(f"{'='*60}\n")
            f.write(chunk["text"])
            f.write("\n\n")
    print(f"Saved {len(all_chunks)} chunks to {output_path}")

if __name__ == "__main__":
    documents = load_documents()
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc["text"], doc["source"])
        all_chunks.extend(chunks)
    
    save_chunks_readable(all_chunks)
    print(f"Total chunks: {len(all_chunks)}")