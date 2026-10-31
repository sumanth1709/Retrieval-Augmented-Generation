import chromadb
import os
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

VECTOR_DB_FOLDER = os.path.join(
    BASE_DIR,
    "vector_db"
)


def load_vector_database():

    client = chromadb.PersistentClient(
        path=VECTOR_DB_FOLDER
    )

    collection = client.get_collection(
        name="rag_documents"
    )

    return collection


def load_embedding_model():

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    return model


def create_query_embedding(model, query):

    query_embedding = model.encode(
        query
    )

    return query_embedding.tolist()


def is_resume_question(query):

    resume_keywords = [
    "resume",
    "cv",
    "curriculum vitae",
    "my skills",
    "my projects",
    "my education",
    "my qualification",
    "my qualifications",
    "my experience",
    "my internship",
    "my certifications",
    "my certification",
    "my programming languages",
    "my technical skills",
    "my technologies",
    "what skills do i have",
    "what projects do i have",
    "what certifications do i have",
    "what certification do i have",
    "what programming languages do i know"
]

    query = query.lower()

    for keyword in resume_keywords:

        if keyword in query:
            return True

    return False


def search_similar_chunks(
    collection,
    query_embedding,
    query,
    top_k=5,
    distance_threshold=1.2
):

    resume_question = is_resume_question(
        query
    )

    if resume_question:

        print(
            "Resume-related question detected."
        )

        print(
            "Searching resume documents..."
        )

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={
                "document_title": "Resume"
            }
        )

        return results

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    filtered_documents = []
    filtered_metadatas = []
    filtered_distances = []

    for index in range(len(documents)):

        if distances[index] <= distance_threshold:

            filtered_documents.append(
                documents[index]
            )

            filtered_metadatas.append(
                metadatas[index]
            )

            filtered_distances.append(
                distances[index]
            )

    results["documents"][0] = filtered_documents
    results["metadatas"][0] = filtered_metadatas
    results["distances"][0] = filtered_distances

    return results


def get_retrieved_context(results):

    documents = results["documents"][0]

    if not documents:

        return ""

    context_parts = []

    for index, document in enumerate(documents):

        context_parts.append(
            f"Source {index + 1}:\n"
            f"{document}"
        )

    context = "\n\n".join(
        context_parts
    )

    return context


def display_results(results):

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print()
    print("=" * 60)
    print("RETRIEVAL RESULTS")
    print("=" * 60)

    if not documents:

        print()
        print(
            "No relevant results found."
        )

        return

    for index in range(len(documents)):

        print()
        print("-" * 60)

        print(
            "Result:",
            index + 1
        )

        print(
            "Distance:",
            distances[index]
        )

        print(
            "Document:",
            metadatas[index]["document_title"]
        )

        print(
            "Page:",
            metadatas[index]["page"]
        )

        print(
            "File type:",
            metadatas[index]["file_type"]
        )

        print(
            "Source:",
            metadatas[index]["source_path"]
        )

        print()
        print("Text:")

        print(
            documents[index]
        )


def main():

    print("=" * 60)
    print("             RAG RETRIEVER")
    print("=" * 60)

    print()
    print("Loading vector database...")

    collection = load_vector_database()

    print(
        "Vectors available:",
        collection.count()
    )

    print()
    print("Loading embedding model...")

    model = load_embedding_model()

    print()
    print("Retriever is ready!")
    print("Type your question.")
    print("Type 'exit' to stop.")

    while True:

        print()

        query = input(
            "Question: "
        ).strip()

        if query.lower() == "exit":

            print(
                "Retriever stopped."
            )

            break

        if not query:

            print(
                "Please enter a question."
            )

            continue

        print()
        print(
            "Creating query embedding..."
        )

        query_embedding = create_query_embedding(
            model,
            query
        )

        print(
            "Searching ChromaDB..."
        )

        results = search_similar_chunks(
            collection,
            query_embedding,
            query,
            top_k=5,
            distance_threshold=1.2
        )

        display_results(
            results
        )

        context = get_retrieved_context(
            results
        )

        print()
        print("=" * 60)
        print("CONTEXT FOR LLM")
        print("=" * 60)

        if context:

            print(
                context
            )

        else:

            print(
                "No relevant context found."
            )


if __name__ == "__main__":

    main()