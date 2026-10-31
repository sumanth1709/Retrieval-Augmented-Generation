import json
import os

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

#Load the embeddings from the JSON file
def load_embeddings():
    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as file:
        embeddings = json.load(file)

    return embeddings

#Check the number of embedded chunks
def main():
    embeddings = load_embeddings()

    print("Total embedded chunks:", len(embeddings))

    first_embedding = embeddings[0]["embedding"]

    print("First embedding dimensions:", len(first_embedding))

    print("First chunk metadata:")
    print("Chunk ID:", embeddings[0]["chunk_id"])
    print("Document:", embeddings[0]["document_title"])
    print("Page:", embeddings[0]["page"])
    print("File type:", embeddings[0]["file_type"])
    print("Source:", embeddings[0]["source_path"])

    print()
    print("First few embedding values:")
    print(first_embedding[:5])


if __name__ == "__main__":
    main()