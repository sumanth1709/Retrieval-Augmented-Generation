import json
import os
from sentence_transformers import SentenceTransformer

#Set the project paths
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

CHUNKS_FILE = os.path.join(
    BASE_DIR,
    "chunks",
    "chunks.json"
)

#Load the chunks from the JSON file
def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    return chunks

#Load the embedding model
def load_embedding_model():
    model = SentenceTransformer("all-MiniLM-L6-v2")

    return model

#Generate embeddings for the chunks
def generate_embeddings(model, chunks):
    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings

#output path
EMBEDDINGS_FILE = os.path.join(
    BASE_DIR,
    "chunks",
    "embeddings.json"
)

#Save the embeddings to a JSON file
def save_embeddings(chunks, embeddings):
    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "document_title": chunk["document_title"],
            "page": chunk["page"],
            "file_type": chunk["file_type"],
            "source_path": chunk["source_path"],
            "text": chunk["text"],
            "embedding": embedding.tolist()
        })

    with open(EMBEDDINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            embedded_chunks,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Embeddings saved:", EMBEDDINGS_FILE)
    
    #Main function to load chunks, generate embeddings, and save them
def main():
    print("Loading chunks...")

    chunks = load_chunks()

    print("Total chunks:", len(chunks))

    print("Loading embedding model...")

    model = load_embedding_model()

    print("Generating embeddings...")

    embeddings = generate_embeddings(
        model,
        chunks
    )

    print("Saving embeddings...")

    save_embeddings(
        chunks,
        embeddings
    )

    print()
    print("Embedding process completed successfully!")


if __name__ == "__main__":
    main()
    