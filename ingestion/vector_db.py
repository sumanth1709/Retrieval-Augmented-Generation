import json
import os
import chromadb


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

EMBEDDINGS_FILE = os.path.join(
    BASE_DIR,
    "chunks",
    "embeddings.json"
)

VECTOR_DB_FOLDER = os.path.join(
    BASE_DIR,
    "vector_db"
)


# ==========================================
# 2. LOAD EMBEDDINGS
# ==========================================

def load_embeddings():
    with open(
        EMBEDDINGS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        embeddings = json.load(file)

    return embeddings


# ==========================================
# 3. CREATE CHROMADB CLIENT
# ==========================================

def create_vector_database():
    os.makedirs(
        VECTOR_DB_FOLDER,
        exist_ok=True
    )

    client = chromadb.PersistentClient(
        path=VECTOR_DB_FOLDER
    )

    return client


# ==========================================
# 4. CREATE COLLECTION
# ==========================================

def create_collection(client):

    collection = client.get_or_create_collection(
        name="rag_documents"
    )

    return collection


# ==========================================
# 5. ADD EMBEDDINGS TO CHROMADB
# ==========================================

def add_embeddings_to_collection(
    collection,
    embedded_chunks
):

    ids = []
    embeddings = []
    documents = []
    metadatas = []

    for chunk in embedded_chunks:

        ids.append(
            str(chunk["chunk_id"])
        )

        embeddings.append(
            chunk["embedding"]
        )

        documents.append(
            chunk["text"]
        )

        metadatas.append({
            "document_title": chunk["document_title"],
            "page": chunk["page"],
            "file_type": chunk["file_type"],
            "source_path": chunk["source_path"]
        })

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )


# ==========================================
# 6. MAIN FUNCTION
# ==========================================

def main():

    print("Loading embeddings...")

    embedded_chunks = load_embeddings()

    print(
        "Total embedded chunks:",
        len(embedded_chunks)
    )

    print("Creating vector database...")

    client = create_vector_database()

    print("Creating collection...")

    collection = create_collection(client)

    print("Adding embeddings to ChromaDB...")

    add_embeddings_to_collection(
        collection,
        embedded_chunks
    )

    print()
    print("Vector database created successfully!")

    print(
        "Total vectors in collection:",
        collection.count()
    )

    print(
        "Vector database location:",
        VECTOR_DB_FOLDER
    )


# ==========================================
# 7. PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()