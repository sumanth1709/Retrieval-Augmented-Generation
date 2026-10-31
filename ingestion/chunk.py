import os
import re
import json
import pymupdf

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")
CHUNKS_FOLDER = os.path.join(BASE_DIR, "chunks")

#cleaning function to remove unwanted characters and whitespace
def clean_text(text):
    # Replace multiple spaces with one space
    text = re.sub(r"[ \t]+", " ", text)

    # Remove too many blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove spaces at the beginning and end
    text = text.strip()

    return text

# read each extracted document
def read_pdf_documents():
    documents = []

    data_folder = os.path.join(BASE_DIR, "data")

    for filename in os.listdir(data_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(data_folder, filename)

            document = pymupdf.open(pdf_path)

            document_title = os.path.splitext(filename)[0]
            file_type = "pdf"
            source_path = os.path.join("data", filename)

            for page_number, page in enumerate(document, start=1):
                text = page.get_text("text")
                text = clean_text(text)

                if text:
                    documents.append({
                        "document_title": document_title,
                        "page": page_number,
                        "file_type": file_type,
                        "source_path": source_path,
                        "text": text
                    })

            document.close()

    return documents

# chunking function to split the text into smaller chunks
def create_chunks(text, chunk_size=500, overlap=50):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start = end - overlap

    return chunks

# process each document and create chunks
def main():
    os.makedirs(CHUNKS_FOLDER, exist_ok=True)

    documents = read_pdf_documents()

    all_chunks = []

    for document in documents:
        document_title = document["document_title"]
        page = document["page"]
        file_type = document["file_type"]
        source_path = document["source_path"]
        text = document["text"]

        chunks = create_chunks(text)

        print()
        print("==============================")
        print("Document:", document_title)
        print("Page:", page)
        print("Chunks created:", len(chunks))
        print("==============================")

        for chunk in chunks:
            all_chunks.append({
                "chunk_id": len(all_chunks),
                "document_title": document_title,
                "page": page,
                "file_type": file_type,
                "source_path": source_path,
                "text": chunk
            })

    output_path = os.path.join(
        CHUNKS_FOLDER,
        "chunks.json"
    )

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            all_chunks,
            file,
            indent=4,
            ensure_ascii=False
        )

    print()
    print("Total chunks:", len(all_chunks))
    print("Saved:", output_path)


if __name__ == "__main__":
    main()